from PyQt6.QtWidgets import QSizePolicy, QPushButton, QHBoxLayout, QLabel


class ActionBarLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = QLabel("Aurora")
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(size_policy)
        self.label.setProperty("class", "action_bar_label")
        self.addWidget(self.label)

        self.addSpacing(100)

        self.profile_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(size_policy)
        self.profile_button.setProperty("class", "action_bar_button")
        self.profile_button.setObjectName("profile_button")
        self.addWidget(self.profile_button)

        self.settings_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(size_policy)
        self.settings_button.setProperty("class", "action_bar_button")
        self.settings_button.setObjectName("settings_button")
        self.addWidget(self.settings_button)

        self.hide_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.hide_button.sizePolicy().hasHeightForWidth())
        self.hide_button.setSizePolicy(size_policy)
        self.hide_button.setProperty("class", "action_bar_button")
        self.hide_button.setObjectName("hide_button")
        self.addWidget(self.hide_button)

        self.exit_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(size_policy)
        self.exit_button.setProperty("class", "action_bar_button")
        self.exit_button.setObjectName("exit_button")
        self.addWidget(self.exit_button)