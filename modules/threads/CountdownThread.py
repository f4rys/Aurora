from PyQt6.QtCore import QThread, pyqtSignal

class CountdownThread(QThread):
    remaining_time =  pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, total_time):
        super().__init__()
        self.total_time = total_time

    def run(self):
        while self.total_time > 0:
            self.sleep(1)
            self.total_time = self.total_time - 1
            self.remaining_time.emit(self.total_time)

        self.finished.emit()