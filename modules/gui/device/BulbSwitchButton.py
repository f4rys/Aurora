from PyQt6.QtWidgets import QPushButton, QSizePolicy


class BulbSwitchButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setProperty("class", "switch")