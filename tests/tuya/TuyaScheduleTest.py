import unittest
from unittest.mock import patch, MagicMock

from modules.tuya.TuyaSchedule import TuyaSchedule


class TuyaScheduleTest(unittest.TestCase):
    def setUp(self):
        self.alias_name = "Test Schedule"
        self.enable = True
        self.time = "12:00"
        self.timezone_id = "UTC"
        self.devices_timers = {"device_1": "timer_1"}
        self.functions = {"function_key": "function_value"}
        self.loops = "1111111"

    @patch('modules.tuya.TuyaSchedule.TuyaCloud')
    def test_save_to_cloud_with_loops(self, MockTuyaCloud):
        """Test saving a schedule with loops to the cloud."""
        mock_tuya_cloud = MockTuyaCloud.return_value
        mock_tuya_cloud.cloud = MagicMock()

        mock_tuya_cloud.cloud.cloudrequest.return_value = {"success": True}

        schedule = TuyaSchedule(
            alias_name=self.alias_name,
            enable=self.enable,
            time=self.time,
            timezone_id=self.timezone_id,
            devices_timers=self.devices_timers,
            functions=self.functions,
            loops=self.loops
        )

        response = schedule.save_to_cloud()
        self.assertTrue(all(response))

        expected_schedule = {
            "alias_name": self.alias_name,
            "time": self.time,
            "timezone_id": self.timezone_id,
            "loops": self.loops,
            "functions": self.functions
        }

        mock_tuya_cloud.cloud.cloudrequest.assert_called_with(
            url="/v2.0/cloud/timer/device/device_1",
            action="POST",
            post=expected_schedule
        )


if __name__ == '__main__':
    unittest.main()
