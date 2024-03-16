from PyQt6.QtWidgets import QSizePolicy, QLabel
from PyQt6.QtCore import Qt

class BulbNameLabel(QLabel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_text(name)
        self.update()

    def set_text(self, text):
        self.setText(text)