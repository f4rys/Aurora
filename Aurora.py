from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMainWindow, QLabel, QWidget, QPushButton

from modules.gui.AuroraStackedWidget import AuroraStackedWidget
from modules.gui.settings.SettingsWidget import SettingsWidget
from modules.gui.all_devices.AllDevicesWidget import AllDevicesWidget
from modules.gui.device.DeviceWidget import DeviceWidget
from modules.gui.NavigationBarWidget import NavigationBarWidget
from modules.gui.scenes.ScenesWidget import ScenesWidget
from modules.gui.schedule.ScheduleWidget import ScheduleWidget
from modules.gui.analytics.AnalyticsWidget import AnalyticsWidget

import modules.resources.resources as resources

  
class Aurora(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.background = QLabel(parent=self.centralwidget)
        self.background.setProperty("class", "background")
        self.background.resize(400, 300)

        self.widget = QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QRect(0, 0, 400, 300))

        self.stackedWidget = AuroraStackedWidget(parent=self.widget)

        self.all_devices = AllDevicesWidget(self)
        self.scenes = ScenesWidget(self)
        self.analytics = AnalyticsWidget(self)
        self.schedule = ScheduleWidget(self)

        self.navigation_bar = NavigationBarWidget(parent=self.widget)
        self.navigation_bar.devices_button.clicked.connect(self.show_all_devices)
        self.navigation_bar.scenes_button.clicked.connect(self.show_scenes)
        self.navigation_bar.schedule_button.clicked.connect(self.show_schedule)
        self.navigation_bar.analytics_button.clicked.connect(self.show_analytics)

        self.settings_button = QPushButton(parent=self.widget)
        self.settings_button.setGeometry(355, 8, 15, 15)
        self.settings_button.setProperty("class", "settings_button")
        self.settings_button.clicked.connect(self.show_settings)

        self.hide_button = QPushButton("⨯", parent=self.widget)
        self.hide_button.setGeometry(370, 0, 25, 25)
        self.hide_button.setProperty("class", "hide_button")
        self.hide_button.clicked.connect(self.hide_window)

        self.stackedWidget.addWidget(self.scenes)
        self.stackedWidget.addWidget(self.schedule)
        self.stackedWidget.addWidget(self.analytics)
        self.stackedWidget.addWidget(self.all_devices)

        self.show_all_devices()

        self.setCentralWidget(self.centralwidget)

    def hide_window(self):
        self.hide()

    def show_window(self):
        screens = QApplication.screens()
        if screens:
            screen_geometry = screens[0].geometry()
            window_width = 400
            window_height = 300
            x = screen_geometry.width() - window_width - screen_geometry.width()//100
            y = screen_geometry.height() - window_height - screen_geometry.height()//20

            self.show()
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(x + window_width//2, y + window_height//2, 0, 0))
            self.animation.setEndValue(QRect(x, y, window_width, window_height))

            self.animation.start()

    def show_settings(self):
        self.settings = SettingsWidget()
        self.stackedWidget.addWidget(self.settings)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.settings))

    def show_device(self, device_id):
        self.device = DeviceWidget(device_id)
        self.stackedWidget.addWidget(self.device)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.device))

    def show_all_devices(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.all_devices))

    def show_scenes(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.scenes))

    def show_schedule(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.schedule))

    def show_analytics(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.analytics))


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    aurora = Aurora()

    with open('styles.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    icon = QIcon(":/icon/icon.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.activated.connect(lambda: aurora.show_window())

    app.exec()
