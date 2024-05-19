from PyQt6.QtCore import QThread, pyqtSignal
from modules.tuya import TuyaAnalytics

class InitiateTuyaAnalyticsThread(QThread):
    finished = pyqtSignal(TuyaAnalytics)

    def run(self):
        try:
            manager = TuyaAnalytics()
            self.finished.emit(manager)
        except Exception:
            self.finished.emit(None)
