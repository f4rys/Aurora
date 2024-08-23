import unittest
from unittest.mock import MagicMock, patch

from modules.gui import MainWindow


class MainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.parent_mock = MagicMock()
        self.main_window = MagicMock(spec=MainWindow)

        self.main_window.main_layout = MagicMock()
        self.main_window.main_layout.stacked_widget = MagicMock()
        self.main_window.main_layout.stacked_widget.currentIndex.return_value = 0
        self.main_window.main_layout.stacked_widget.indexOf.side_effect = lambda widget: 0

        self.main_window.navigation_bar_layout = MagicMock()
        self.main_window.navigation_bar_layout.devices_button = MagicMock()
        self.main_window.navigation_bar_layout.smart_mode_button = MagicMock()

        self.main_window.action_bar_layout = MagicMock()
        self.main_window.action_bar_layout.label = MagicMock()
        self.main_window.dictionary = {"credentials_title": "Expected Title"}

    def test_initialization(self):
        """Test that MainWindow initializes correctly with the default geometry."""
        self.main_window.geometry.return_value.width.return_value = 400
        self.main_window.geometry.return_value.height.return_value = 300

        self.assertIsNotNone(self.main_window)
        self.assertEqual(self.main_window.geometry().width(), 400)
        self.assertEqual(self.main_window.geometry().height(), 300)

    def test_show_all_devices(self):
        """Test that MainWindow can show all devices."""
        with patch('modules.tuya.check_credentials', return_value=True):
            self.main_window.show_all_devices()
            self.assertEqual(self.main_window.main_layout.stacked_widget.currentIndex(),
                             self.main_window.main_layout.stacked_widget.indexOf(self.main_window.main_layout.stacked_widget.all_devices))

    def test_show_smart_mode(self):
        """Test that MainWindow can show the smart mode view."""
        self.main_window.show_smart_mode()
        self.assertEqual(self.main_window.main_layout.stacked_widget.currentIndex(),
                         self.main_window.main_layout.stacked_widget.indexOf(self.main_window.main_layout.stacked_widget.smart_mode))

    def test_show_help(self):
        """Test that MainWindow can show the help view."""
        self.main_window.show_help()
        self.assertEqual(self.main_window.main_layout.stacked_widget.currentIndex(),
                         self.main_window.main_layout.stacked_widget.indexOf(self.main_window.main_layout.stacked_widget.help))

    def test_enable_buttons(self):
        """Test that MainWindow can enable navigation buttons."""
        self.main_window.enable_buttons()
        self.assertTrue(self.main_window.navigation_bar_layout.devices_button.isEnabled())
        self.assertTrue(self.main_window.navigation_bar_layout.smart_mode_button.isEnabled())


if __name__ == '__main__':
    unittest.main()
