import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtWidgets import QApplication

from modules.threads import InitiateTuyaSchedulesManagerThread
from modules.gui.schedules import SchedulesWidget
from modules.tuya import TuyaSchedulesManager


class SchedulesWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget = SchedulesWidget(self.parent_mock)
        manager = TuyaSchedulesManager("general")
        self.widget.update_ui(manager)

    def test_create_list_initial_state(self):
        """Test the initial state of the schedule list."""
        self.widget.create_list()
        self.assertIsNotNone(self.widget.vlayout.count())

    @patch.object(InitiateTuyaSchedulesManagerThread, 'start')
    def test_create_list_starts_thread(self, mock_start):
        """Test that creating the list starts the background thread."""
        self.widget.create_list()
        mock_start.assert_called_once()

    def test_add_schedule_calls_edit_schedule(self):
        """Test that adding a schedule calls the edit schedule method."""
        self.widget.add_schedule()
        self.parent_mock.parent.parent.show_edit_schedule.assert_called_once()

    def test_delete_schedule_calls_remove_from_cloud(self):
        """Test that deleting a schedule calls the remove_from_cloud method."""
        schedule_mock = MagicMock()
        schedule_mock.remove_from_cloud.return_value = [True]

        self.widget.delete_schedule(schedule_mock)
        schedule_mock.remove_from_cloud.assert_called_once()

    def test_delete_schedule_error_handling(self):
        """Test error handling when delete schedule fails."""
        schedule_mock = MagicMock()
        schedule_mock.remove_from_cloud.return_value = [False]

        with patch('modules.gui.schedules.SchedulesWidget.show_error_toast') as mock_show_error:
            self.widget.delete_schedule(schedule_mock)
            mock_show_error.assert_called_once()

    def test_delete_add_schedule_button(self):
        """Test deleting the add schedule button from the layout."""
        self.widget.delete_add_schedule_button()
        self.assertEqual(self.widget.main_layout.count(), 1)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == '__main__':
    unittest.main()
