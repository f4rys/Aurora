import json
import shutil
import os

import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication

from modules.gui.credentials import CredentialsWidget

class CredentialsWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        mock_parent = MagicMock()
        mock_parent.parent.parent.parent.restart_window = MagicMock()
        cls.widget = CredentialsWidget(parent=mock_parent)
        cls.original_file = 'tinytuya.json'
        cls.backup_file = 'tinytuya_backup.json'

        shutil.copy(cls.original_file, cls.backup_file)

    @classmethod
    def tearDownClass(cls):
        shutil.copy(cls.backup_file, cls.original_file)
        os.remove(cls.backup_file)

    def test_set_credentials(self):
        """Tests the set_credentials method of the CredentialsWidget class."""
        self.widget.set_credentials("valid_api_key", "valid_api_secret", "eu", "valid_device_id")
        self.assertEqual(self.widget.api_key_input.text(), "valid_api_key")
        self.assertEqual(self.widget.api_secret_input.text(), "valid_api_secret")
        self.assertEqual(self.widget.api_device_id_input.text(), "valid_device_id")
        self.assertEqual(self.widget.api_region_input.currentText(), self.widget.dictionary["central_europe_dc"])

    def test_send_credentials_success(self):
        """Tests the send_credentials method of the CredentialsWidget class with valid credentials."""
        with open('tinytuya.json', 'r', encoding="utf-8") as file:
            credentials = json.load(file)

        api_key = credentials.get("apiKey")
        api_secret = credentials.get("apiSecret")
        api_device_id = credentials.get("apiDeviceId")

        with patch('modules.tuya.register', return_value=True):
            self.widget.api_key_input.setText(api_key)
            self.widget.api_secret_input.setText(api_secret)
            self.widget.api_device_id_input.setText(api_device_id)
            self.widget.api_region_input.setCurrentIndex(3)

            toast = MagicMock()
            with patch('modules.gui.credentials.CredentialsWidget.Toast', return_value=toast):
                self.widget.send_credentials()

            toast.setTitle.assert_called_with(self.widget.dictionary["success_toast_title"])
            toast.setText.assert_called_with(self.widget.dictionary["success_toast_body_credentials"])
            toast.show.assert_called_once()

    def test_send_credentials_failure(self):
        """Tests the send_credentials method of the CredentialsWidget class with invalid credentials."""
        with patch('modules.tuya.register', return_value=False):
            self.widget.api_key_input.setText("invalid_api_key")
            self.widget.api_secret_input.setText("invalid_api_secret")
            self.widget.api_device_id_input.setText("invalid_device_id")
            self.widget.api_region_input.setCurrentIndex(3)

            toast = MagicMock()
            with patch('modules.gui.credentials.CredentialsWidget.Toast', return_value=toast):
                self.widget.send_credentials()

            toast.setTitle.assert_called_with(self.widget.dictionary["error_toast_title"])
            toast.setText.assert_called_with(self.widget.dictionary["error_toast_body_credentials"])
            toast.show.assert_called_once()

            self.assertEqual(self.widget.api_key_input.text(), "")
            self.assertEqual(self.widget.api_secret_input.text(), "")
            self.assertEqual(self.widget.api_device_id_input.text(), "")
            self.assertEqual(self.widget.api_region_input.currentIndex(), 3)

if __name__ == '__main__':
    unittest.main()
