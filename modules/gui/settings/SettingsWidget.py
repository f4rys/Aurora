from configparser import ConfigParser
import os

from PyQt6.QtWidgets import QWidget, QCheckBox, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel

from modules.dictionaries.loader import load_dictionary


class SettingsWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        self.config = ConfigParser()
        self.config.read('settings.ini')

        mode = self.config.get("General", "smart_mode")
        language = self.config.get("GUI", "interface_language")
        max_retry = self.config.get("General", "max_retry")

        self.smart_mode_label = QLabel(self.dictionary["smart_mode_label"])

        self.smart_mode = QCheckBox(self)
        self.smart_mode.setText(self.dictionary["smart_mode_settings"])
        self.smart_mode.stateChanged.connect(self.switch_smart_mode)

        if mode == 'on':
            self.smart_mode.setChecked(True)
        else:
            self.smart_mode.setChecked(False)

        self.language_label = QLabel(self.dictionary["language_label"])

        self.language = QComboBox(self)
        self.language.addItems(["English", "Polski"])

        if language == 'en':
            self.language.setCurrentIndex(self.language.findText("English"))
        if language == 'pl':
            self.language.setCurrentIndex(self.language.findText("Polski"))

        self.language.activated.connect(self.change_language)

        self.max_retry_label = QLabel(self.dictionary["max_retry_label"])

        self.max_retry = QComboBox(self)
        self.max_retry.addItems([
            "0" + ' - ' + self.dictionary["max_retry_0"], 
            "1", 
            "2", 
            "3" + ' - ' + self.dictionary["max_retry_3"], 
            "4", 
            "5" + ' - ' + self.dictionary["max_retry_5"]
            ])
        self.max_retry.setCurrentIndex(int(max_retry))
        self.max_retry.activated.connect(self.change_max_retry)

        self.vlayout.addWidget(self.smart_mode_label)
        self.vlayout.addWidget(self.smart_mode)
        self.vlayout.addWidget(self.language_label)
        self.vlayout.addWidget(self.language)
        self.vlayout.addWidget(self.max_retry_label)
        self.vlayout.addWidget(self.max_retry)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

    def change_max_retry(self, val):
        self.config.set("General", "max_retry", str(val))

        if os.path.exists("settings.ini"):
            with open('settings.ini', 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)

    def change_language(self, val):
        if val == 0:
            language = 'en'
        if val == 1:
            language = 'pl'

        self.config.set("GUI", "interface_language", language)
        if os.path.exists("settings.ini"):
            with open('settings.ini', 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)

        self.parent.parent.parent.restart()

    def switch_smart_mode(self, val):
        if val:
            smart_mode = "on"
        else:
            smart_mode = "off"

        self.config.set("General", "smart_mode", smart_mode)
        if os.path.exists("settings.ini"):
            with open('settings.ini', 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)

        # If off, delete all schedules from cloud