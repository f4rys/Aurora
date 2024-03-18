from PyQt6.QtWidgets import QWidget, QTimeEdit, QPushButton, QVBoxLayout

from modules.dictionaries.loader import load_dictionary


class TimerTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")

        self.accept_button = QPushButton(self.dictionary["set_timer"])
        self.accept_button.clicked.connect(self.on_accept)
        self.accept_button.setProperty("class", "timer_button")
        self.accept_button.setFlat(True)
        
        self.vlayout.addWidget(self.time_edit)
        self.vlayout.addWidget(self.accept_button)

    def on_accept(self):
        selected_time = self.time_edit.time()
