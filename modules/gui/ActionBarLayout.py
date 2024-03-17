from PyQt6.QtWidgets import QSizePolicy, QPushButton, QHBoxLayout

class ActionBarLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pushbutton_settings = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_settings.sizePolicy().hasHeightForWidth())
        self.pushbutton_settings.setSizePolicy(sizePolicy)
        self.pushbutton_settings.setProperty("class", "settings_button")
        self.addWidget(self.pushbutton_settings)

        self.pushbutton_hide = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_hide.sizePolicy().hasHeightForWidth())
        self.pushbutton_hide.setSizePolicy(sizePolicy)
        self.pushbutton_hide.setProperty("class", "hide_button")
        self.addWidget(self.pushbutton_hide)