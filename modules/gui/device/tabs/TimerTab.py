from PyQt6.QtWidgets import QWidget, QTimeEdit, QPushButton, QVBoxLayout

from modules import dictionary


class TimerTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout(self)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")

        self.accept_button = QPushButton(dictionary["set_timer"])
        self.accept_button.clicked.connect(self.on_accept)
        self.accept_button.setProperty("class", "timer_button")
        self.accept_button.setFlat(True)
        
        self.vlayout.addWidget(self.time_edit)
        self.vlayout.addWidget(self.accept_button)

    def on_accept(self):
        selected_time = self.time_edit.time()
