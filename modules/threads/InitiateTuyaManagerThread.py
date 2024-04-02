from PyQt6.QtCore import QThread, pyqtSignal
from modules.tuya import TuyaManager

class InitiateTuyaManagerThread(QThread):
    finished = pyqtSignal(TuyaManager)

    def run(self):
        try:
            manager = TuyaManager()
            self.finished.emit(manager)
        except Exception as e:
            self.finished.emit(None)
