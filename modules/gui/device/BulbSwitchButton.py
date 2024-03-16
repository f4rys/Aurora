from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QPushButton, QSizePolicy

class BulbSwitchButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setProperty("class", "switch")
        self.setStyleSheet("image : url(:/device/bulb_on.png);")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)