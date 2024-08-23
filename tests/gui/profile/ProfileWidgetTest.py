import os
import shutil
import unittest
from unittest.mock import MagicMock, mock_open, patch

from PyQt6.QtWidgets import QApplication

from modules.gui.profile import ProfileWidget


class ProfileWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget = ProfileWidget(self.parent_mock)

        self.backup_file_path = 'tinytuya_backup.json'
        self.original_file_path = 'tinytuya.json'
        if os.path.exists(self.original_file_path):
            shutil.copy(self.original_file_path, self.backup_file_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"apiKey": "key", "apiSecret": "secret", "apiRegion": "region", "apiDeviceID": "device_id"}')
    def test_get_credentials_existing_file(self, mock_open, mock_exists):
        """Test retrieving credentials from an existing file"""
        mock_exists.return_value = True
        api_key, api_secret, api_region, api_device_id = self.widget.get_credentials()
        self.assertEqual(api_key, "key")
        self.assertEqual(api_secret, "secret")
        self.assertEqual(api_region, "region")
        self.assertEqual(api_device_id, "device_id")

    @patch('os.path.exists')
    def test_get_credentials_non_existing_file(self, mock_exists):
        """Test retrieving credentials when the file does not exist"""
        mock_exists.return_value = False
        api_key, api_secret, api_region, api_device_id = self.widget.get_credentials()
        self.assertEqual(api_key, "")
        self.assertEqual(api_secret, "")
        self.assertEqual(api_region, "")
        self.assertEqual(api_device_id, "")

    @patch('modules.tuya.register')
    def test_fetch_data_success(self, mock_register):
        """Test the fetch data functionality when registration is successful"""
        mock_register.return_value = True
        self.widget.api_key, self.widget.api_secret, self.widget.api_region, self.widget.api_device_id = "key", "secret", "region", "device_id"
        with patch('pyqttoast.Toast.show') as mock_show:
            self.widget.fetch_data()
            mock_show.assert_called_once()

    @patch('modules.tuya.register')
    def test_fetch_data_failure(self, mock_register):
        """Test the fetch data functionality when registration fails"""
        mock_register.return_value = False
        self.widget.api_key, self.widget.api_secret, self.widget.api_region, self.widget.api_device_id = "key", "secret", "region", "device_id"
        with patch('pyqttoast.Toast.show') as mock_show:
            self.widget.fetch_data()
            mock_show.assert_called_once()

    def tearDown(self):
        if os.path.exists(self.backup_file_path):
            shutil.copy(self.backup_file_path, self.original_file_path)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app
        if os.path.exists('tinytuya_backup.json'):
            os.remove('tinytuya_backup.json')


if __name__ == '__main__':
    unittest.main()
