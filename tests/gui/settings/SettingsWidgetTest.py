import os
import shutil
import unittest
from unittest.mock import MagicMock, patch, mock_open

from PyQt6.QtWidgets import QApplication

from modules.gui.settings import SettingsWidget


class SettingsWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the QApplication object
        cls.app = QApplication([])
        cls.parent_mock = MagicMock()
        cls.widget = SettingsWidget(cls.parent_mock)

        # Paths for the original and backup settings file
        cls.original_settings_path = 'settings.ini'
        cls.backup_settings_path = 'settings_backup.ini'

        # Create a backup of the settings file before tests run
        if os.path.exists(cls.original_settings_path):
            shutil.copy(cls.original_settings_path, cls.backup_settings_path)

    @patch('builtins.open', new_callable=mock_open)
    def test_change_max_retry(self, mock_file):
        """Test changing the maximum retry setting."""
        self.widget.change_max_retry(2)
        self.assertEqual(self.widget.config.get("General", "max_retry"), "2")
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_change_language_to_english(self, mock_file):
        """Test changing the language setting to English."""
        self.widget.change_language(0)
        self.assertEqual(self.widget.config.get("GUI", "interface_language"), 'en')
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_change_language_to_polish(self, mock_file):
        """Test changing the language setting to Polish."""
        self.widget.change_language(1)
        self.assertEqual(self.widget.config.get("GUI", "interface_language"), 'pl')
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('os.remove')
    def test_switch_smart_mode_on(self, mock_remove):
        """Test switching smart mode on."""
        self.widget.switch_smart_mode(True)
        self.assertEqual(self.widget.config.get("General", "smart_mode"), "on")
        mock_remove.assert_not_called()

    @patch('os.remove')
    def test_switch_smart_mode_off(self, mock_remove):
        """Test switching smart mode off."""
        self.widget.switch_smart_mode(False)
        self.assertEqual(self.widget.config.get("General", "smart_mode"), "off")

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists(cls.backup_settings_path):
                shutil.copy(cls.backup_settings_path, cls.original_settings_path)
        finally:
            if os.path.exists(cls.backup_settings_path):
                os.remove(cls.backup_settings_path)

        cls.app.quit()
        del cls.app
        del cls.parent_mock
        del cls.widget
        del cls.original_settings_path
        del cls.backup_settings_path


if __name__ == '__main__':
    unittest.main()
