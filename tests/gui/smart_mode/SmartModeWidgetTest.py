import unittest
from unittest.mock import patch, MagicMock

from PyQt6.QtWidgets import QApplication

from modules.gui.smart_mode import SmartModeWidget


class SmartModeWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.widget = SmartModeWidget()

    @patch('modules.dictionaries.loader.load_dictionary')
    def test_initialization(self, mock_load_dictionary):
        """Test widget initialization."""
        mock_load_dictionary.return_value = {
            "smart_mode_off": "Smart mode is off",
            "computing_smart_mode": "Computing smart mode",
            "no_more_actions": "No more actions"
        }
        self.assertIsNotNone(self.widget)
        self.assertIsInstance(self.widget, SmartModeWidget)

    @patch('configparser.ConfigParser.get')
    def test_check_settings_smart_mode_on(self, mock_get):
        """Test smart mode on settings check."""
        mock_get.return_value = 'on'
        self.widget.check_settings()
        self.assertIn("Calculating smart mode suggestions..", self.widget.vlayout.itemAt(0).widget().text())

    @patch('configparser.ConfigParser.get')
    def test_check_settings_smart_mode_off(self, mock_get):
        """Test smart mode off settings check."""
        mock_get.return_value = 'off'
        self.widget.check_settings()
        self.assertIn("Smart mode is off.", self.widget.vlayout.itemAt(0).widget().text())

    @patch('modules.threads.InitiateTuyaSmartModeThread')
    def test_get_tuya_smart_mode(self, mock_thread):
        """Test fetching Tuya smart mode."""
        mock_thread.return_value = MagicMock()
        self.widget.get_tuya_smart_mode()
        self.assertTrue(self.widget.thread_worker.isRunning())

    @patch('modules.threads.InitiateTuyaSmartModeThread')
    def test_init_ui(self, mock_thread):
        """Test initializing UI."""
        mock_thread.return_value.finished.connect(lambda: self.widget.init_ui([]))
        self.widget.init_ui([])
        self.assertIn("No more actions planned for today.", self.widget.vlayout.itemAt(0).widget().text())

    def tearDown(self):
        if hasattr(self.widget, 'thread_worker') and self.widget.thread_worker.isRunning():
            self.widget.thread_worker.quit()
            self.widget.thread_worker.wait()

        self.widget.deleteLater()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
