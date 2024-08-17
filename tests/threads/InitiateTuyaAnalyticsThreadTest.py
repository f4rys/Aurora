import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtCore import QThread
from modules.threads import InitiateTuyaAnalyticsThread
from modules.tuya import TuyaAnalytics

class InitiateTuyaAnalyticsThreadTest(unittest.TestCase):
    @patch('modules.tuya.TuyaAnalytics')
    def test_run_success(self, MockTuyaAnalytics):
        """Test that the thread successfully initializes TuyaAnalytics and emits the manager upon completion."""
        thread = InitiateTuyaAnalyticsThread()
        MockTuyaAnalytics.return_value = MagicMock(spec=TuyaAnalytics)
        thread.finished.connect(lambda manager: self.assertIsInstance(manager, TuyaAnalytics))
        thread.start()
        thread.quit()
        thread.wait()

    @patch('modules.tuya.TuyaAnalytics')
    def test_run_failure(self, MockTuyaAnalytics):
        """Test that the thread emits None upon failure to initialize TuyaAnalytics."""
        MockTuyaAnalytics.side_effect = Exception("Initialization failed")
        thread = InitiateTuyaAnalyticsThread()
        thread.finished.connect(lambda manager: self.assertIsNone(manager))
        thread.start()
        thread.quit()
        thread.wait()

    def test_thread_is_instance_of_QThread(self):
        """Test that the thread is an instance of QThread."""
        thread = InitiateTuyaAnalyticsThread()
        self.assertIsInstance(thread, QThread)

if __name__ == '__main__':
    unittest.main()
