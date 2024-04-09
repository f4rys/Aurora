import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTimeEdit, QPushButton, QVBoxLayout, QLabel, QSizePolicy

from modules.dictionaries.loader import load_dictionary
from modules.threads import CountdownThread


class CountdownTab(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("mm:ss")
        self.time_edit.setToolTip(self.dictionary["time_edit_tooltip"])

        self.accept_button = QPushButton(self.dictionary["set_countdown"])
        self.accept_button.clicked.connect(self.on_accept)
        self.accept_button.setProperty("class", "countdown_button")
        self.accept_button.setFlat(True)
        self.accept_button.setToolTip(self.dictionary["countdown_accept_button_tooltip"])

        self.remaining_time_label = QLabel()
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.remaining_time_label.setSizePolicy(size_policy)
        self.remaining_time_label.setScaledContents(False)
        self.remaining_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vlayout.addWidget(self.time_edit)
        self.vlayout.addWidget(self.accept_button)

    def on_accept(self):
        selected_time = self.time_edit.time()
        time_in_sec = selected_time.minute()*60 + selected_time.second()
        self.parent.device.set_countdown(time_in_sec)

        self.thread_worker = CountdownThread(time_in_sec)
        self.thread_worker.finished.connect(self.timer_complete)
        self.thread_worker.remaining_time.connect(self.print_time)
        self.thread_worker.start()
        self.vlayout.addWidget(self.remaining_time_label)

    def timer_complete(self):
        self.remaining_time_label.setText("")
        self.vlayout.removeWidget(self.remaining_time_label)
        time.sleep(1)
        self.parent.change_icon()

    def print_time(self, remaining_time):
        hours = remaining_time // 3600
        remaining_seconds = remaining_time % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        self.remaining_time_label.setText(f"Remaining time: h: {hours}, m: {minutes}, s: {seconds}")
