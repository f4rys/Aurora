import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

from PyQt6.QtWidgets import QApplication

from modules.gui.schedules import EditScheduleWidget


class EditScheduleWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget = EditScheduleWidget(self.parent_mock)
        schedule_mock = MagicMock()
        schedule_mock.alias_name = "Test Schedule"
        schedule_mock.time = "12:00"
        schedule_mock.loops = "1100000"
        schedule_mock.devices_timers = {"1": "1234"}

        self.widget.init_ui(schedule_mock, new=True)

    def test_init_ui(self):
        """Test UI initialization with schedule mock data."""
        self.assertEqual(self.widget.name_edit.text(), "Test Schedule")
        self.assertEqual(self.widget.time_edit.time().toString(), "12:00:00")

    def test_set_time(self):
        """Test setting time from schedule data."""
        self.widget.schedule = MagicMock()
        self.widget.schedule.time = "15:30"
        self.widget.set_time()
        self.assertEqual(self.widget.time_edit.time().toString(), "15:30:00")

    def test_load_weekdays(self):
        """Test loading weekday settings from schedule loops."""
        self.widget.schedule = MagicMock()
        self.widget.schedule.loops = "1100000"
        for button in self.widget.weekdays_group.buttons():
            self.widget.weekdays_group.removeButton(button)
        self.widget.load_weekdays()

        checked_buttons = [button.isChecked() for button in self.widget.weekdays_group.buttons()]
        self.assertEqual(checked_buttons, [True, True, False, False, False, False, False])

    def test_load_devices(self):
        """Test loading device list from a mock file."""
        mock_devices_data = json.dumps([{"id": "1", "name": "Device 1"}])

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', new_callable=mock_open, read_data=mock_devices_data):
            self.widget.load_devices()

            self.assertEqual(len(self.widget.devices_group.buttons()), 1)
            self.assertEqual(self.widget.devices_group.buttons()[0].text(), "Device 1")

    def test_get_ranges(self):
        """Test retrieving range data for device settings."""
        mock_button = MagicMock()
        mock_button.objectName.return_value = "device_id"
        mock_button.isChecked.return_value = True

        self.widget.devices_group.buttons = MagicMock(return_value=[mock_button])

        mock_data = '[{ "id": "device_id", "mapping": {"22": {"values": {"min": 2, "max": 100}}, "23": {"values": {"min": 5, "max": 120}}, "24": {"values": {"h": {"min": 4,"max": 360}, "s": {"min": 10,"max": 200}, "v": {"min": 50,"max": 1000}}}}}]'

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', new_callable=mock_open, read_data=mock_data):
            ranges = self.widget.get_ranges()
            self.assertIn("brightness", ranges)
            self.assertIn(2, ranges["brightness"]["min"])
            self.assertIn(100, ranges["brightness"]["max"])
            self.assertIn(5, ranges["temperature"]["min"])
            self.assertIn(120, ranges["temperature"]["max"])
            self.assertIn(4, ranges["h"]["min"])
            self.assertIn(360, ranges["h"]["max"])
            self.assertIn(10, ranges["s"]["min"])
            self.assertIn(200, ranges["s"]["max"])
            self.assertIn(50, ranges["v"]["min"])
            self.assertIn(1000, ranges["v"]["max"])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
