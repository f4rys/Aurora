from configparser import ConfigParser

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QCheckBox, QComboBox

from modules import dictionary


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigParser()
        self.config.read('settings.ini')

        mode = self.config.get("General", "smart_mode")
        language = self.config.get("GUI", "interface_language")

        self.smart_mode = QCheckBox(self)
        self.smart_mode.setText(dictionary["smart_mode"])
        self.smart_mode.setGeometry(QRect(10, 10, 200, 30))

        if(mode == 'on'):
            self.smart_mode.setChecked(True)
        else:
            self.smart_mode.setChecked(False)

        self.language = QComboBox(self)
        self.language.addItems(["English", "Polski"])
        self.language.setGeometry(QRect(10, 50, 200, 30))

        if language == 'en':
            self.language.setCurrentIndex(self.language.findText("English"))
        if language == 'pl':
            self.language.setCurrentIndex(self.language.findText("Polski"))

        self.language.activated.connect(self.change_language)


    def change_language(self, val):
        if val == 0: language = 'en'
        if val == 1: language = 'pl'

        self.config.set("GUI", "interface_language", language)

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)