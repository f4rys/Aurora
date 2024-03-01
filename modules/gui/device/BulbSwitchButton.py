from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QPushButton

class BulbSwitchButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(QRect(50, 10, 91, 91))
        self.setProperty("class", "switch")