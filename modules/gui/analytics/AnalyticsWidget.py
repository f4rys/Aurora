from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QLabel

class AnalyticsWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.label = QLabel("Analytics", parent=self)
        self.label.setGeometry(QRect(10, 10, 50, 23))
