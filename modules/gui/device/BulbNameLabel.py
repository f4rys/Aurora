from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy, QLabel

from modules.dictionaries.loader import load_dictionary


class BulbNameLabel(QLabel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setToolTip(self.dictionary["bulb_label_tooltip"])

        self.set_text(name)
        self.update()

    def set_text(self, text):
        self.setText(text)