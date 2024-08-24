import unittest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, date
import os

import pandas as pd

from modules.tuya import TuyaSmartMode


class TuyaSmartModeTest(unittest.TestCase):
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    @patch.object(TuyaSmartMode, 'smart_mode')
    @patch.object(TuyaSmartMode, 'delete_used_schedules')
    def test_initialization_creates_prediction_file(self, mock_delete, mock_smart_mode, mock_makedirs, mock_open, mock_exists):
        """Test that initialization creates the prediction file if it does not exist."""
        mock_exists.return_value = False
        TuyaSmartMode()
        mock_makedirs.assert_called_once_with(os.path.dirname(r"modules\resources\json\predictions.json"), exist_ok=True)
        mock_open.assert_called_once_with(r"modules\resources\json\predictions.json", 'w', encoding="utf-8")
        mock_delete.assert_called_once()
        mock_smart_mode.assert_called_once()

    @patch('modules.tuya.TuyaSmartMode.TuyaSchedulesManager')
    @patch('modules.tuya.TuyaSmartMode.date')
    @patch('modules.tuya.TuyaSmartMode.datetime')
    def test_delete_used_schedules(self, mock_datetime, mock_date, mock_tuya_schedules_manager):
        """Test deletion of schedules that are past the current date."""
        fixed_today = date(2024, 1, 2)
        fixed_now = datetime(2024, 1, 2, 12, 0, 0)

        mock_date.today.return_value = fixed_today
        mock_datetime.now.return_value = fixed_now
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        mock_manager_instance = mock_tuya_schedules_manager.return_value

        mock_manager_instance.schedules = [
            MagicMock(date="20240404", time="10:00"),
            MagicMock(date="20230101", time="10:00")
        ]

        smart_mode = TuyaSmartMode()

        smart_mode.delete_used_schedules()

        mock_manager_instance.schedules[1].remove_from_cloud.assert_called()
        mock_manager_instance.schedules[0].remove_from_cloud.assert_not_called()

    @patch('os.listdir')
    @patch('os.path.join')
    @patch('pandas.read_json')
    def test_create_dataframe(self, mock_read_json, mock_path_join, mock_listdir):
        """Test creation of a DataFrame from JSON log files."""
        mock_listdir.return_value = ['log1.json', 'log2.json']
        mock_path_join.side_effect = lambda directory, filename: f"{directory}/{filename}"
        mock_read_json.return_value = pd.DataFrame({
            'code': ['switch_led', 'bright_value_v2', 'temp_value_v2', 'colour_data_v2'],
            'event_time': ['2024-01-01T10:00:00', '2024-01-01T11:00:00', '2024-01-01T12:00:00', '2024-01-01T13:00:00'],
            'value': ['true', '500', '300', 'ff0000']
        })

        smart_mode = TuyaSmartMode()
        df = smart_mode.create_dataframe()

        self.assertIn('device_id', df.columns)

    def test_hex_to_hsv(self):
        """Test conversion from hex color to HSV values."""
        smart_mode = TuyaSmartMode()
        hsv = smart_mode.hex_to_hsv('ff0000')
        self.assertEqual(hsv, {'h': 0.0, 's': 1000.0, 'v': 1000.0})

    def test_hex_to_rgb(self):
        """Test conversion from hex color to average RGB value."""
        smart_mode = TuyaSmartMode()
        avg_rgb = smart_mode.hex_to_rgb('ff0000')
        self.assertEqual(avg_rgb, 85)


if __name__ == '__main__':
    unittest.main()
