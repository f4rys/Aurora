from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QLabel


class SmartModeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = QLabel("Smart mode", parent=self)
        self.label.setGeometry(QRect(10, 10, 50, 23))