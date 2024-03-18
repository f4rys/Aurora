from PyQt6.QtWidgets import QSizePolicy, QPushButton, QHBoxLayout, QLabel


class ActionBarLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = QLabel("Aurora")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setProperty("class", "action_bar_label")
        self.addWidget(self.label)

        self.addSpacing(100)

        self.pushbutton_profile = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_profile.sizePolicy().hasHeightForWidth())
        self.pushbutton_profile.setSizePolicy(sizePolicy)
        self.pushbutton_profile.setProperty("class", "action_bar_button")
        self.pushbutton_profile.setObjectName("profile_button")
        self.addWidget(self.pushbutton_profile)

        self.pushbutton_settings = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_settings.sizePolicy().hasHeightForWidth())
        self.pushbutton_settings.setSizePolicy(sizePolicy)
        self.pushbutton_settings.setProperty("class", "action_bar_button")
        self.pushbutton_settings.setObjectName("settings_button")
        self.addWidget(self.pushbutton_settings)

        self.pushbutton_hide = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_hide.sizePolicy().hasHeightForWidth())
        self.pushbutton_hide.setSizePolicy(sizePolicy)
        self.pushbutton_hide.setProperty("class", "action_bar_button")
        self.pushbutton_hide.setObjectName("hide_button")
        self.addWidget(self.pushbutton_hide)

        self.pushbutton_exit = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_exit.sizePolicy().hasHeightForWidth())
        self.pushbutton_exit.setSizePolicy(sizePolicy)
        self.pushbutton_exit.setProperty("class", "action_bar_button")
        self.pushbutton_exit.setObjectName("exit_button")
        self.addWidget(self.pushbutton_exit)