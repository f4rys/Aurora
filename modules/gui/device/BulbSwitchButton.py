from PyQt6.QtWidgets import QPushButton, QSizePolicy

from modules.dictionaries.loader import load_dictionary

class BulbSwitchButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setToolTip(self.dictionary["bulb_tooltip"])
        self.setProperty("class", "switch")

    def set_icon(self, state):
        if state:
            self.setStyleSheet("image : url(:/device/bulb_on.png);")
        else:
            self.setStyleSheet("image : url(:/device/bulb_off.png);")

        self.update()
        self.repaint()