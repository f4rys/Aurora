import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtCore import QThread
from modules.threads import InitiateTuyaManagerThread
from modules.tuya import TuyaManager

class InitiateTuyaManagerThreadTest(unittest.TestCase):
    @patch('modules.tuya.TuyaManager')
    def test_run_success(self, MockTuyaManager):
        """Test that the thread successfully initializes TuyaManager and emits the manager upon completion."""
        thread = InitiateTuyaManagerThread()
        MockTuyaManager.return_value = MagicMock(spec=TuyaManager)
        thread.finished.connect(lambda manager: self.assertIsInstance(manager, TuyaManager))
        thread.start()
        thread.quit()
        thread.wait()

    @patch('modules.tuya.TuyaManager')
    def test_run_failure(self, MockTuyaManager):
        """Test that the thread emits None upon failure to initialize TuyaManager."""
        MockTuyaManager.side_effect = Exception("Initialization failed")
        thread = InitiateTuyaManagerThread()
        thread.finished.connect(lambda manager: self.assertIsNone(manager))
        thread.start()
        thread.quit()
        thread.wait()

    def test_thread_is_instance_of_QThread(self):
        """Test that the thread is an instance of QThread."""
        thread = InitiateTuyaManagerThread()
        self.assertIsInstance(thread, QThread)

if __name__ == '__main__':
    unittest.main()
