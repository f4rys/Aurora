from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy, QLabel


class BulbNameLabel(QLabel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_text(name)
        self.update()

    def set_text(self, text):
        self.setText(text)