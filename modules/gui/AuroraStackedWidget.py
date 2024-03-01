from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QStackedWidget

class AuroraStackedWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(QRect(100, 30, 300, 270))
        self.setMouseTracking(False)
        self.setAutoFillBackground(False)