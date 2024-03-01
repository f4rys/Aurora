from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QTimeEdit, QPushButton

class TimerTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setGeometry(QRect(25,10,150,20))

        self.accept_button = QPushButton("Set the timer", self)
        self.accept_button.clicked.connect(self.on_accept)
        self.accept_button.setGeometry(QRect(25,40,150,20))

    def on_accept(self):
        selected_time = self.time_edit.time()
        pass
