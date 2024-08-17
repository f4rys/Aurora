import unittest
from PyQt6.QtCore import QCoreApplication
from modules.threads import CountdownThread

class CountdownThreadTest(unittest.TestCase):
    def setUp(self):
        self.app = QCoreApplication([])
        self.thread = CountdownThread(total_time=5)

    def test_initial_total_time(self):
        """Test that the initial total time is set correctly."""
        self.assertEqual(self.thread.total_time, 5)

    def test_remaining_time_signal(self):
        """Test that the remaining_time signal is emitted correctly."""
        self.thread.start()
        self.thread.remaining_time.connect(lambda time: self.assertIn(time, [4, 3, 2, 1, 0]))
        self.thread.wait()

    def test_thread_finishes_after_countdown(self):
        """Test that the thread finishes after the countdown."""
        self.thread.start()
        self.thread.finished.connect(lambda: self.assertFalse(self.thread.isRunning()))
        self.thread.wait()

    def test_stop_function(self):
        """Test that the stop function works correctly."""
        self.thread.start()
        self.thread.stop()
        self.assertFalse(self.thread.runs)

    def test_zero_total_time(self):
        """Test that the thread finishes immediately if total_time is zero."""
        zero_thread = CountdownThread(total_time=0)
        zero_thread.start()
        zero_thread.finished.connect(lambda: self.assertFalse(zero_thread.isRunning()))
        zero_thread.wait()

    def tearDown(self):
        self.thread.quit()
        self.thread.wait()

if __name__ == '__main__':
    unittest.main()
