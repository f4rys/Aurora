import unittest
from unittest.mock import patch
from modules.tuya.register import register, CONFIGFILE


class RegisterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_content = None
        try:
            with open(CONFIGFILE, 'r', encoding="utf-8") as f:
                cls.original_content = f.read()
        except FileNotFoundError:
            pass

    @patch('tinytuya.Cloud')
    def test_register_cloud_error(self, mock_cloud):
        """Test register function when Cloud returns an error."""
        mock_cloud.return_value.error = "Some cloud error"
        result = register('test_api_key', 'test_api_secret', 'test_region', 'test_device_id')
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls):
        if cls.original_content:
            with open(CONFIGFILE, 'w', encoding="utf-8") as f:
                f.write(cls.original_content)


if __name__ == '__main__':
    unittest.main()
