import unittest
from unittest.mock import patch, MagicMock
import json
import os

from modules.tuya.TuyaAnalytics import TuyaAnalytics


class TuyaAnalyticsTest(unittest.TestCase):
    @patch('modules.tuya.TuyaAnalytics.TuyaCloud')
    def test_get_devices_logs_new_logs(self, mock_tuya_cloud):
        """Test logs are created for new device logs."""
        mock_cloud = MagicMock()
        mock_tuya_cloud.return_value.cloud = mock_cloud
        mock_cloud.getdevicelog.return_value = {'result': {'logs': [{'event_time': 12345, 'data': 'some_data'}]}}

        with open("devices.json", "w", encoding="utf-8") as f:
            json.dump([{'id': 'device1'}], f)

        tuya_analytics = TuyaAnalytics()
        tuya_analytics.get_devices_logs()

        with open('modules/resources/json/logs/device1.json', 'r', encoding="utf-8") as f:
            logs_data = json.load(f)
        self.assertEqual(logs_data, [{'event_time': 12345, 'data': 'some_data'}])

        os.remove("devices.json")
        os.remove('modules/resources/json/logs/device1.json')

    @patch('modules.tuya.TuyaAnalytics.TuyaCloud')
    def test_get_devices_logs_existing_logs(self, mock_tuya_cloud):
        """Test logs are appended to existing device logs."""
        mock_cloud = MagicMock()
        mock_tuya_cloud.return_value.cloud = mock_cloud
        mock_cloud.getdevicelog.return_value = {'result': {'logs': [
            {'event_time': 12345, 'data': 'some_data'},
            {'event_time': 67890, 'data': 'new_data'}
        ]}}

        with open("devices.json", "w", encoding="utf-8") as f:
            json.dump([{'id': 'device1'}], f)
        os.makedirs('modules/resources/json/logs', exist_ok=True)
        with open('modules/resources/json/logs/device1.json', 'w', encoding="utf-8") as f:
            json.dump([{'event_time': 12345, 'data': 'some_data'}], f)

        tuya_analytics = TuyaAnalytics()
        tuya_analytics.get_devices_logs()

        with open('modules/resources/json/logs/device1.json', 'r', encoding="utf-8") as f:
            logs_data = json.load(f)
        self.assertEqual(logs_data, [
            {'event_time': 12345, 'data': 'some_data'},
            {'event_time': 67890, 'data': 'new_data'}
        ])

        os.remove("devices.json")
        os.remove('modules/resources/json/logs/device1.json')

    def test_create_plot_with_data(self):
        """Test plot creation with valid data."""
        os.makedirs('modules/resources/json/logs', exist_ok=True)
        with open('modules/resources/json/logs/device1.json', 'w', encoding="utf-8") as f:
            json.dump([
                {'event_time': 1691660800000, 'data': 'some_data'},
                {'event_time': 1691747200000, 'data': 'some_data'},
                {'event_time': 1691747200000, 'data': 'some_data'}
            ], f)

        tuya_analytics = TuyaAnalytics()
        figure = tuya_analytics.create_plot(['device1'])

        self.assertIsNotNone(figure)

        os.remove('modules/resources/json/logs/device1.json')

    def test_create_plot_no_data(self):
        """Test plot creation with no data."""
        tuya_analytics = TuyaAnalytics()
        figure = tuya_analytics.create_plot(['non_existent_device'])

        self.assertIsNone(figure)


if __name__ == '__main__':
    unittest.main()
