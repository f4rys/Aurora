from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QLabel


class ProfileWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Profile", parent=self)
        self.label.setGeometry(QRect(10, 10, 50, 23))
