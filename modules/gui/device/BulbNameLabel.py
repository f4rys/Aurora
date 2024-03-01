from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QRect

class BulbNameLabel(QLabel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(QRect(60, 120, 100, 23))
        self.set_text(name)
        self.update()

    def set_text(self, text):
        self.setText(text)