import unittest
from unittest.mock import patch, mock_open
from modules.tuya.register import check_credentials, CONFIGFILE


class CheckCredentialsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_content = None
        try:
            with open(CONFIGFILE, 'r') as f:
                cls.original_content = f.read()
        except FileNotFoundError:
            pass

    @patch('builtins.open', new_callable=mock_open, read_data='{"apiKey": "key", "apiSecret": "secret", "apiRegion": "region"}')
    def test_check_credentials_valid(self, mock_open_file):
        """Test check_credentials with valid config data."""
        result = check_credentials()
        self.assertTrue(result)
        mock_open_file.assert_called_once_with(CONFIGFILE, encoding="utf-8")

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_check_credentials_empty(self, mock_open_file):
        """Test check_credentials with empty config data."""
        result = check_credentials()
        self.assertFalse(result)
        mock_open_file.assert_called_once_with(CONFIGFILE, encoding="utf-8")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_check_credentials_missing_file(self, mock_open_file):
        """Test check_credentials when the config file is missing."""
        result = check_credentials()
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls):
        if cls.original_content:
            with open(CONFIGFILE, 'w') as f:
                f.write(cls.original_content)


if __name__ == '__main__':
    unittest.main()
