from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QMetaObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout, QHBoxLayout, QSizePolicy, QSystemTrayIcon

from modules.gui.NavigationBarLayout import NavigationBarLayout
from modules.gui.AuroraStackedWidget import AuroraStackedWidget
from modules.gui.settings.SettingsWidget import SettingsWidget

import modules.resources.resources as resources


class Aurora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 300)

        font = QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(9)
        font.setBold(False)
        self.setFont(font)

        self.centralwidget = QWidget(parent=self)

        self.background = QLabel(parent=self.centralwidget)
        self.background.setProperty("class", "background")
        self.background.resize(400, 300)

        self.gridLayoutWidget = QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 400, 300))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.navigation_bar_layout = NavigationBarLayout()
        self.navigation_bar_layout.pushbutton_devices.clicked.connect(self.show_all_devices)
        self.navigation_bar_layout.pushbutton_scenes.clicked.connect(self.show_scenes)
        self.navigation_bar_layout.pushbutton_analytics.clicked.connect(self.show_analytics)
        self.navigation_bar_layout.pushbutton_schedule.clicked.connect(self.show_schedule)
        self.gridLayout.addLayout(self.navigation_bar_layout, 2, 0, 5, 1)

        self.horizontalLayout = QHBoxLayout()

        self.pushbutton_settings = QPushButton(parent=self.gridLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_settings.sizePolicy().hasHeightForWidth())
        self.pushbutton_settings.setSizePolicy(sizePolicy)
        self.pushbutton_settings.setProperty("class", "settings_button")
        self.horizontalLayout.addWidget(self.pushbutton_settings)
        self.pushbutton_settings.clicked.connect(self.show_settings)

        self.pushbutton_hide = QPushButton(parent=self.gridLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_hide.sizePolicy().hasHeightForWidth())
        self.pushbutton_hide.setSizePolicy(sizePolicy)
        self.pushbutton_hide.setProperty("class", "hide_button")
        self.horizontalLayout.addWidget(self.pushbutton_hide)
        self.pushbutton_hide.clicked.connect(self.hide_window)

        self.gridLayout.addLayout(self.horizontalLayout, 2, 4, 1, 1)

        self.stackedWidget = AuroraStackedWidget()

        self.gridLayout.addWidget(self.stackedWidget, 3, 1, 4, 4)
        self.setCentralWidget(self.centralwidget)
    
        QMetaObject.connectSlotsByName(self)

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

    def show_all_devices(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.stackedWidget.all_devices))

    def show_scenes(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.stackedWidget.scenes))

    def show_analytics(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.stackedWidget.analytics))

    def show_schedule(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.stackedWidget.schedule))

    def show_settings(self):
        self.settings = SettingsWidget()
        self.stackedWidget.addWidget(self.settings)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.settings))

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
