from PyQt6.QtCore import QThread, pyqtSignal
from modules.tuya import TuyaSchedulesManager

class InitiateTuyaSchedulesManagerThread(QThread):
    finished = pyqtSignal(TuyaSchedulesManager)

    def run(self):
        try:
            manager = TuyaSchedulesManager()
            self.finished.emit(manager)
        except Exception:
            self.finished.emit(None)