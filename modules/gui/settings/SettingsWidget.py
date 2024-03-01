from configparser import ConfigParser
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QCheckBox, QComboBox

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        config = ConfigParser()
        config.read('settings.ini')
        mode = config.get("General", "smart_mode")

        self.smart_mode = QCheckBox(self)
        self.smart_mode.setText("Smart Mode")
        self.smart_mode.setGeometry(QRect(10, 10, 200, 30))

        if(mode == 'on'):
            self.smart_mode.setChecked(True)
        else:
            self.smart_mode.setChecked(False)

        self.language = QComboBox(self)
        self.language.addItems(["English", "Polski"])
        self.language.setGeometry(QRect(10, 50, 200, 30))