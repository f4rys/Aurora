from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy, QPushButton, QHBoxLayout, QLabel

from modules.dictionaries.loader import load_dictionary

class ActionBarLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.setContentsMargins(30, 8, 10, 0)

        self.button_group = QHBoxLayout()
        self.button_group.setContentsMargins(0, 0, 0, 0)
        self.button_group.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.label = QLabel()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(size_policy)
        self.label.setProperty("class", "action_bar_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.label)

        self.profile_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.profile_button.sizePolicy().hasHeightForWidth())
        self.profile_button.setSizePolicy(size_policy)
        self.profile_button.setProperty("class", "action_bar_button")
        self.profile_button.setObjectName("profile_button")
        self.profile_button.setToolTip(self.dictionary["profile_tooltip"])
        self.button_group.addWidget(self.profile_button)

        self.settings_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(size_policy)
        self.settings_button.setProperty("class", "action_bar_button")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setToolTip(self.dictionary["settings_tooltip"])
        self.button_group.addWidget(self.settings_button)

        self.hide_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.hide_button.sizePolicy().hasHeightForWidth())
        self.hide_button.setSizePolicy(size_policy)
        self.hide_button.setProperty("class", "action_bar_button")
        self.hide_button.setObjectName("hide_button")
        self.hide_button.setToolTip(self.dictionary["hide_tooltip"])
        self.button_group.addWidget(self.hide_button)

        self.exit_button = QPushButton()
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(size_policy)
        self.exit_button.setProperty("class", "action_bar_button")
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setToolTip(self.dictionary["exit_tooltip"])
        self.button_group.addWidget(self.exit_button)

        self.addLayout(self.button_group)

    def set_label(self, text):
        self.label.setText(text)
