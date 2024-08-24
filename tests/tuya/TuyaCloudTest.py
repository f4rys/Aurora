import unittest
from unittest.mock import patch, MagicMock, mock_open
import requests
from modules.tuya import TuyaCloud


class TuyaCloudTest(unittest.TestCase):
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"apiKey": "test_key", "apiSecret": "test_secret", "apiRegion": "us", "apiDeviceID": "test_device_id"}')
    def test_initialization_with_credentials(self, mock_open, mock_exists):
        """Test initialization with valid credentials."""
        mock_exists.return_value = True
        tuya_cloud = TuyaCloud()
        self.assertEqual(tuya_cloud.api_key, "test_key")
        self.assertEqual(tuya_cloud.api_secret, "test_secret")
        self.assertEqual(tuya_cloud.api_region, "us")
        self.assertEqual(tuya_cloud.api_device_id, "test_device_id")
        self.assertIsNotNone(tuya_cloud.cloud)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_initialization_with_missing_credentials(self, mock_open, mock_exists):
        """Test initialization with missing credentials."""
        mock_exists.return_value = False
        tuya_cloud = TuyaCloud()
        self.assertEqual(tuya_cloud.api_key, "")
        self.assertEqual(tuya_cloud.api_secret, "")
        self.assertEqual(tuya_cloud.api_region, "")
        self.assertEqual(tuya_cloud.api_device_id, "")
        self.assertIsNone(tuya_cloud.cloud)

    @patch('requests.delete')
    @patch('time.time', return_value=1633072800)
    def test_request_on_cloud_delete(self, mock_time, mock_delete):
        """Test DELETE request to the cloud."""
        tuya_cloud = TuyaCloud()
        mock_delete.return_value.status_code = 200
        response = tuya_cloud.request_on_cloud('DELETE', '/test/url', None)
        self.assertEqual(response.status_code, 200)
        mock_delete.assert_called_once()

    @patch('requests.put')
    @patch('time.time', return_value=1633072800)
    def test_request_on_cloud_put(self, mock_time, mock_put):
        """Test PUT request to the cloud."""
        tuya_cloud = TuyaCloud()
        mock_put.return_value.status_code = 200
        response = tuya_cloud.request_on_cloud('PUT', '/test/url', None, body={"key": "value"})
        self.assertEqual(response.status_code, 200)
        mock_put.assert_called_once()

    @patch('requests.get')
    @patch('time.time', return_value=1633072800)
    def test_request_on_cloud_get(self, mock_time, mock_get):
        """Test GET request to the cloud."""
        tuya_cloud = TuyaCloud()
        mock_get.return_value = MagicMock(status_code=200)
        response = tuya_cloud.request_on_cloud('GET', '/test/url', None)
        self.assertEqual(response, "")
        mock_get.assert_called_once()

    @patch('requests.get')
    @patch('requests.put')
    @patch('requests.delete')
    @patch('time.time', return_value=1633072800)
    def test_request_on_cloud_invalid_action(self, mock_time, mock_delete, mock_put, mock_get):
        """Test handling of invalid action in cloud request."""
        tuya_cloud = TuyaCloud()

        response = tuya_cloud.request_on_cloud('INVALID_ACTION', '/test/url', None)

        self.assertEqual(response, "")

    @patch('requests.get')
    @patch('time.time', return_value=1633072800)
    def test_request_on_cloud_with_invalid_url(self, mock_time, mock_get):
        """Test handling of invalid URL in cloud request."""
        tuya_cloud = TuyaCloud()

        mock_get.side_effect = requests.exceptions.RequestException("Invalid URL")

        response = tuya_cloud.request_on_cloud('GET', '/invalid/url', None)

        self.assertEqual(response, "")


if __name__ == '__main__':
    unittest.main()
