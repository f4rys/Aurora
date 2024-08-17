import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtCore import QThread
from modules.threads import InitiateTuyaSchedulesManagerThread
from modules.tuya import TuyaSchedulesManager

class InitiateTuyaSchedulesManagerThreadTest(unittest.TestCase):
    @patch('modules.tuya.TuyaSchedulesManager')
    def test_run_success(self, MockTuyaSchedulesManager):
        """Test that the thread successfully initializes TuyaSchedulesManager and emits the manager upon completion."""
        thread = InitiateTuyaSchedulesManagerThread()
        MockTuyaSchedulesManager.return_value = MagicMock(spec=TuyaSchedulesManager)
        thread.finished.connect(lambda manager: self.assertIsInstance(manager, TuyaSchedulesManager))
        thread.start()
        thread.quit()
        thread.wait()

    @patch('modules.tuya.TuyaSchedulesManager')
    def test_run_failure(self, MockTuyaSchedulesManager):
        """Test that the thread emits None upon failure to initialize TuyaSchedulesManager."""
        MockTuyaSchedulesManager.side_effect = Exception("Initialization failed")
        thread = InitiateTuyaSchedulesManagerThread()
        thread.finished.connect(lambda manager: self.assertIsNone(manager))
        thread.start()
        thread.quit()
        thread.wait()

    def test_thread_is_instance_of_QThread(self):
        """Test that the thread is an instance of QThread."""
        thread = InitiateTuyaSchedulesManagerThread()
        self.assertIsInstance(thread, QThread)

if __name__ == '__main__':
    unittest.main()
