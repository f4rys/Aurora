from PyQt6.QtCore import QRect
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton

class NavigationBarWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(QRect(0, 0, 100, 300))

        self.devices_button = QPushButton("All devices", parent=self)
        self.devices_button.setProperty("class", "tab_button")
        self.devices_button.setIcon(QIcon(":/navigation/devices.png"))
        self.devices_button.setGeometry(QRect(10, 80, 85, 30))

        self.scenes_button = QPushButton("Scenes", parent=self)
        self.scenes_button.setProperty("class", "tab_button")
        self.scenes_button.setIcon(QIcon(":/navigation/scenes.png"))
        self.scenes_button.setGeometry(QRect(10, 120, 85, 30))

        self.analytics_button = QPushButton("Analytics", parent=self)
        self.analytics_button.setProperty("class", "tab_button")
        self.analytics_button.setIcon(QIcon(":/navigation/analytics.png"))
        self.analytics_button.setGeometry(QRect(10, 160, 85, 30))

        self.schedule_button = QPushButton("Schedule", parent=self)
        self.schedule_button.setProperty("class", "tab_button")
        self.schedule_button.setIcon(QIcon(":/navigation/schedule.png"))
        self.schedule_button.setGeometry(QRect(10, 200, 85, 30))

