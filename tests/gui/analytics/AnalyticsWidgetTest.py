import os
import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QApplication

from modules.gui.analytics import AnalyticsWidget
from modules.tuya import TuyaAnalytics


class AnalyticsWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.widget = AnalyticsWidget(None)
        cls.analytics = TuyaAnalytics()
        cls.widget.init_ui(cls.analytics)

    def test_load_devices_with_invalid_file(self):
        """Tests the load_devices method with an invalid file."""
        if os.path.exists("devices.json"):
            os.remove("devices.json")
        self.widget.load_devices()
        self.assertEqual(len(self.widget.button_group.buttons()), 0)

    def test_select_all(self):
        """Tests the select_all method of the AnalyticsWidget class."""
        self.widget.load_devices()
        self.widget.select_all()
        for button in self.widget.button_group.buttons():
            self.assertTrue(button.isChecked())

    def test_deselect_all(self):
        """Tests the deselect_all method of the AnalyticsWidget class."""
        self.widget.load_devices()
        self.widget.select_all()
        self.widget.deselect_all()
        for button in self.widget.button_group.buttons():
            self.assertFalse(button.isChecked())

    @patch('modules.threads.InitiateTuyaAnalyticsThread')
    def test_init_ui_with_analytics(self, mock_thread):
        """Tests the init_ui method of the AnalyticsWidget class with analytics."""
        mock_thread.return_value.finished.connect = MagicMock()
        mock_thread.return_value.start = MagicMock()
        mock_thread.return_value.finished.emit = MagicMock()

        mock_analytics = MagicMock()
        self.widget.init_ui(mock_analytics)
        self.assertIsNotNone(self.widget.tuya_analytics)

    def test_update_plot_with_checked_buttons(self):
        """Tests the update_plot method of the AnalyticsWidget class with checked buttons."""
        self.widget.load_devices()
        self.widget.select_all()
        self.widget.update_plot()
        self.assertEqual(self.widget.plotlayout.count(), 1)

    def test_update_plot_with_no_checked_buttons(self):
        """Tests the update_plot method of the AnalyticsWidget class with no checked buttons."""
        self.widget.load_devices()
        self.widget.deselect_all()
        self.widget.update_plot()
        self.assertEqual(self.widget.plotlayout.count(), 1)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app
        del cls.widget
        del cls.analytics


if __name__ == "__main__":
    unittest.main()
