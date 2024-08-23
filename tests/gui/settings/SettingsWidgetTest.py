import os
import shutil
import unittest
from unittest.mock import MagicMock, patch, mock_open

from PyQt6.QtWidgets import QApplication

from modules.gui.settings import SettingsWidget


class SettingsWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget = SettingsWidget(self.parent_mock)

        self.original_settings_path = 'settings.ini'
        self.backup_settings_path = 'settings_backup.ini'
        if os.path.exists(self.original_settings_path):
            shutil.copy(self.original_settings_path, self.backup_settings_path)

    @patch('builtins.open', new_callable=mock_open)
    def test_change_max_retry(self, mock_file):
        self.widget.change_max_retry(2)
        self.assertEqual(self.widget.config.get("General", "max_retry"), "2")
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_change_language_to_english(self, mock_file):
        self.widget.change_language(0)
        self.assertEqual(self.widget.config.get("GUI", "interface_language"), 'en')
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_change_language_to_polish(self, mock_file):
        self.widget.change_language(1)
        self.assertEqual(self.widget.config.get("GUI", "interface_language"), 'pl')
        mock_file.assert_called_once_with('settings.ini', 'w', encoding='utf-8')

    @patch('os.remove')
    def test_switch_smart_mode_on(self, mock_remove):
        self.widget.switch_smart_mode(True)
        self.assertEqual(self.widget.config.get("General", "smart_mode"), "on")
        mock_remove.assert_not_called()

    @patch('os.remove')
    def test_switch_smart_mode_off(self, mock_remove):
        self.widget.switch_smart_mode(False)
        self.assertEqual(self.widget.config.get("General", "smart_mode"), "off")
        mock_remove.assert_called_once_with(r"modules\resources\json\predictions.json")

    def tearDown(self):
        if os.path.exists(self.backup_settings_path):
            shutil.copy(self.backup_settings_path, self.original_settings_path)
        if os.path.exists(self.backup_settings_path):
            os.remove(self.backup_settings_path)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
