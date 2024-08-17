import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtCore import QThread
from modules.threads import InitiateTuyaSmartModeThread
from modules.tuya import TuyaSmartMode

class InitiateTuyaSmartModeThreadTest(unittest.TestCase):
    @patch('modules.tuya.TuyaSmartMode')
    def test_run_success(self, MockTuyaSmartMode):
        """Test that the thread successfully initializes TuyaSmartMode and emits the manager upon completion."""
        thread = InitiateTuyaSmartModeThread()
        MockTuyaSmartMode.return_value = MagicMock(spec=TuyaSmartMode)
        thread.finished.connect(lambda manager: self.assertIsInstance(manager, TuyaSmartMode))
        thread.start()
        thread.quit()
        thread.wait()

    @patch('modules.tuya.TuyaSmartMode')
    def test_run_failure(self, MockTuyaSmartMode):
        """Test that the thread emits None upon failure to initialize TuyaSmartMode."""
        MockTuyaSmartMode.side_effect = Exception("Initialization failed")
        thread = InitiateTuyaSmartModeThread()
        thread.finished.connect(lambda manager: self.assertIsNone(manager))
        thread.start()
        thread.quit()
        thread.wait()

    def test_thread_is_instance_of_QThread(self):
        """Test that the thread is an instance of QThread."""
        thread = InitiateTuyaSmartModeThread()
        self.assertIsInstance(thread, QThread)

if __name__ == '__main__':
    unittest.main()
