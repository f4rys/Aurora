import unittest
from unittest.mock import patch, mock_open
import json

from modules.tuya import TuyaManager


class TuyaManagerTest(unittest.TestCase):
    @patch('modules.tuya.TuyaManager.deviceScan')
    @patch('modules.tuya.TuyaManager.ConfigParser')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_import_devices(self, mock_exists, mock_open_file, mock_config_parser, mock_device_scan):
        """Test importing and initializing active devices."""
        mock_config = mock_config_parser.return_value
        mock_config.get.return_value = '0'

        mock_device_scan.return_value = {
            'device1': {
                'id': '12345',
                'key': 'local_key',
                'version': '3.3',
                'name': 'Test Device',
                'ip': '192.168.1.2'
            }
        }

        devices_json_content = [
            {
                "id": "12345",
                "name": "Test Device",
                "icon": "http://example.com/icon.png",
                "mapping": {
                    "22": {"values": {"min": 10, "max": 1000}},
                    "23": {"values": {"min": 2500, "max": 6500}},
                    "24": {"values": {"h": {"min": 0, "max": 360}, "s": {"min": 0, "max": 1000}, "v": {"min": 0, "max": 1000}}},
                    "26": {"values": {"min": 0, "max": 86400}}
                }
            }
        ]

        mock_open_file.return_value.read.return_value = json.dumps(devices_json_content)

        manager = TuyaManager()

        self.assertIn('12345', manager.active_devices)
        self.assertEqual(manager.active_devices['12345'].id, '12345')
        self.assertEqual(manager.active_devices['12345'].name, 'Test Device')
        self.assertEqual(manager.active_devices['12345'].icon_link, "http://example.com/icon.png")
        self.assertEqual(manager.active_devices['12345'].brightness_range, [10, 1000])
        self.assertEqual(manager.active_devices['12345'].temperature_range, [2500, 6500])
        self.assertTrue(manager.active_devices['12345'].is_rgb)
        self.assertTrue(manager.active_devices['12345'].has_countdown)

    @patch('modules.tuya.TuyaManager.deviceScan')
    @patch('modules.tuya.TuyaManager.ConfigParser')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_inactive_devices(self, mock_exists, mock_open_file, mock_config_parser, mock_device_scan):
        """Test handling of inactive devices."""
        mock_config = mock_config_parser.return_value
        mock_config.get.return_value = '0'

        mock_device_scan.return_value = {}

        devices_json_content = [
            {
                "id": "54321",
                "name": "Inactive Device",
                "icon": "http://example.com/icon2.png",
                "mapping": {
                    "22": {"values": {"min": 10, "max": 1000}},
                    "23": {"values": {"min": 2500, "max": 6500}}
                }
            }
        ]

        mock_open_file.return_value.read.return_value = json.dumps(devices_json_content)

        manager = TuyaManager()

        self.assertIn('54321', manager.inactive_devices)
        self.assertEqual(manager.inactive_devices['54321']['name'], 'Inactive Device')
        self.assertEqual(manager.inactive_devices['54321']['icon_link'], "http://example.com/icon2.png")


if __name__ == '__main__':
    unittest.main()
