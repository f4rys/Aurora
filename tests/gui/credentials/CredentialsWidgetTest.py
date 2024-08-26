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

    def test_set_credentials(self):
        """Tests the set_credentials method of the CredentialsWidget class."""
        self.widget.set_credentials("valid_api_key", "valid_api_secret", "eu", "valid_device_id")
        self.assertEqual(self.widget.api_key_input.text(), "valid_api_key")
        self.assertEqual(self.widget.api_secret_input.text(), "valid_api_secret")
        self.assertEqual(self.widget.api_device_id_input.text(), "valid_device_id")
        self.assertEqual(self.widget.api_region_input.currentText(), self.widget.dictionary["central_europe_dc"])

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

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
