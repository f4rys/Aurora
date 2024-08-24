import unittest
from unittest.mock import patch, MagicMock

from modules.tuya import TuyaSchedulesManager


class TuyaSchedulesManagerTest(unittest.TestCase):
    @patch('modules.tuya.TuyaSchedulesManager.TuyaCloud')
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_initialization_with_devices(self, mock_open, mock_exists, mock_tuya_cloud):
        """Test initialization with devices and schedules returned from the cloud."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = MagicMock(read=MagicMock(return_value='[{"id": "device1"}]'))

        mock_tuya_cloud.return_value.cloud.cloudrequest.return_value = {
            "result": [
                {"alias_name": "Schedule 1", "enable": True, "time": "08:00", "timezone_id": "UTC", "loops": "1111111", "category": "", "timer_id": "timer1", "devices_timers": {}, "functions": []}
            ]
        }

        manager = TuyaSchedulesManager(category="general")

        self.assertEqual(len(manager.schedules), 1)
        self.assertEqual(manager.schedules[0].alias_name, "Schedule 1")
        self.assertTrue(manager.schedules[0].enable)

    @patch('modules.tuya.TuyaSchedulesManager.TuyaCloud')
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_initialization_with_no_devices(self, mock_open, mock_exists, mock_tuya_cloud):
        """Test initialization with no devices listed."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = MagicMock(read=MagicMock(return_value='[]'))

        manager = TuyaSchedulesManager(category="general")
        self.assertEqual(len(manager.schedules), 0)

    @patch('modules.tuya.TuyaSchedulesManager.TuyaCloud')
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_no_response_from_cloud(self, mock_open, mock_exists, mock_tuya_cloud):
        """Test handling when there is no response from the cloud."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = MagicMock(read=MagicMock(return_value='[{"id": "device1"}]'))

        mock_tuya_cloud.return_value.cloud.cloudrequest.return_value = None

        manager = TuyaSchedulesManager(category="general")
        self.assertEqual(len(manager.schedules), 0)

    @patch('modules.tuya.TuyaSchedulesManager.TuyaCloud')
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_category_smart_mode(self, mock_open, mock_exists, mock_tuya_cloud):
        """Test initialization with schedules for the 'smart_mode' category."""
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = MagicMock(read=MagicMock(return_value='[{"id": "device1"}]'))

        mock_tuya_cloud.return_value.cloud.cloudrequest.return_value = {
            "result": [
                {"alias_name": "Smart Mode Schedule", "enable": True, "time": "09:00", "timezone_id": "UTC", "loops": "0000000", "category": "smart_mode", "timer_id": "timer2", "devices_timers": {}, "functions": [], "date": "2023-10-10"}
            ]
        }

        manager = TuyaSchedulesManager(category="smart_mode")
        self.assertEqual(len(manager.schedules), 1)
        self.assertEqual(manager.schedules[0].alias_name, "Smart Mode Schedule")
        self.assertEqual(manager.schedules[0].category, "smart_mode")


if __name__ == '__main__':
    unittest.main()
