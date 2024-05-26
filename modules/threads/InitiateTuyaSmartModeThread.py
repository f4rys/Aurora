from PyQt6.QtCore import QThread, pyqtSignal
from modules.tuya import TuyaSmartMode

class InitiateTuyaSmartModeThread(QThread):
    finished = pyqtSignal(TuyaSmartMode)

    def run(self):
        try:
            manager = TuyaSmartMode()
            self.finished.emit(manager)
        except Exception:
            self.finished.emit(None)
