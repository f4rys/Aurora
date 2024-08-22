import sys
import unittest
from unittest.mock import MagicMock, patch

from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QApplication

from modules.gui.device.tabs import CountdownTab


class CountdownTabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.parent = MagicMock()
        self.parent.device.read_current_countdown.return_value = 0
        self.parent.device.countdown_range = [0, 3600]
        self.parent.device.set_countdown = MagicMock()
        self.parent.device.cancel_countdown = MagicMock()
        self.parent.device.delete_countdown = MagicMock()
        self.parent.change_icon = MagicMock()

        self.countdown_tab = CountdownTab(self.parent)

    def test_initialization(self):
        """Test the initial state and properties of the CountdownTab."""
        self.assertIsInstance(self.countdown_tab, CountdownTab)
        self.assertEqual(self.countdown_tab.time_edit.displayFormat(), "HH:mm:ss")
        self.assertEqual(self.countdown_tab.accept_button.text(), "Set countdown")

    def test_on_accept_valid_time(self):
        """Test accepting a valid countdown time."""
        self.countdown_tab.time_edit.setTime(QTime(0, 1, 30))
        self.countdown_tab.on_accept()
        self.parent.device.set_countdown.assert_called_once_with(90)
        self.assertEqual(self.countdown_tab.accept_button.text(), "Cancel countdown")

    def test_on_accept_zero_time(self):
        """Test accepting a countdown time of zero."""
        self.countdown_tab.time_edit.setTime(QTime(0, 0, 0))
        self.countdown_tab.on_accept()
        self.parent.device.set_countdown.assert_called_once_with(0)

    @patch('modules.gui.device.tabs.CountdownTab.CountdownThread')
    def test_countdown_on(self, MockCountdownThread):
        """Test starting the countdown with a valid time."""
        mock_thread = MockCountdownThread.return_value
        mock_thread.start = MagicMock()

        self.countdown_tab.countdown_on(90)
        self.assertEqual(self.countdown_tab.accept_button.text(), "Cancel countdown")
        mock_thread.start.assert_called_once()

    @patch('modules.gui.device.tabs.CountdownTab.CountdownThread')
    def test_cancel_countdown(self, MockCountdownThread):
        """Test cancelling an ongoing countdown."""
        mock_thread = MockCountdownThread.return_value
        self.countdown_tab.thread_worker = mock_thread

        self.countdown_tab.countdown_on(90)

        self.countdown_tab.cancel_countdown()
        self.assertEqual(self.countdown_tab.parent.device.cancel_countdown.call_count, 1)
        mock_thread.stop.assert_called_once()

    def test_timer_complete(self):
        """Test behavior when the countdown timer completes."""
        self.countdown_tab.timer_complete()
        self.parent.change_icon.assert_called_once()
        self.assertEqual(self.countdown_tab.accept_button.text(), "Set countdown")

    def test_print_time(self):
        """Test the display of the remaining time."""
        self.countdown_tab.print_time(3661)
        self.assertEqual(self.countdown_tab.remaining_time_label.text(), "Remaining time: 01:01:01")

    def test_sec_to_hms(self):
        """Test conversion from seconds to hours, minutes, and seconds."""
        hours, minutes, seconds = self.countdown_tab.sec_to_hms(3661)
        self.assertEqual((hours, minutes, seconds), (1, 1, 1))

    def test_countdown_off(self):
        """Test turning off the countdown timer."""
        self.countdown_tab.countdown_off()
        self.assertEqual(self.countdown_tab.remaining_time_label.text(), "")
        self.assertEqual(self.countdown_tab.accept_button.text(), "Set countdown")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == '__main__':
    unittest.main()
