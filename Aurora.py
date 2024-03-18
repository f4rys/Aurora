from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QMetaObject
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QSystemTrayIcon, QFrame

from modules.gui import NavigationBarLayout, AuroraStackedWidget, SettingsWidget, ActionBarLayout, ProfileWidget
from modules.resources import resources


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

        self.central_widget = QWidget(parent=self)

        self.background = QLabel(parent=self.central_widget)
        self.background.setProperty("class", "background")
        self.background.resize(400, 300)

        self.grid_widget = QWidget(parent=self.central_widget)
        self.grid_widget.setGeometry(QRect(0, 0, 400, 300))

        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.navigation_bar_layout = NavigationBarLayout()
        self.navigation_bar_layout.devices_button.clicked.connect(self.show_all_devices)
        self.navigation_bar_layout.scenes_button.clicked.connect(self.show_scenes)
        self.navigation_bar_layout.analytics_button.clicked.connect(self.show_analytics)
        self.navigation_bar_layout.schedule_button.clicked.connect(self.show_schedule)
        self.navigation_bar_layout.help_button.clicked.connect(self.show_help)
        self.grid_layout.addLayout(self.navigation_bar_layout, 2, 0, 5, 1)

        self.vertical_line = QFrame(parent=self.grid_widget)
        self.vertical_line.setFrameShape(QFrame.Shape.VLine)
        self.vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.vertical_line.setProperty("class", "vline")
        self.grid_layout.addWidget(self.vertical_line, 2, 1, 5, 1)

        self.action_bar_layout = ActionBarLayout()
        self.action_bar_layout.profile_button.clicked.connect(self.show_profile)
        self.action_bar_layout.settings_button.clicked.connect(self.show_settings)
        self.action_bar_layout.hide_button.clicked.connect(self.hide_window)
        self.action_bar_layout.exit_button.clicked.connect(self.exit)
        self.grid_layout.addLayout(self.action_bar_layout, 2, 4, 1, 1)

        self.stacked_widget = AuroraStackedWidget()

        self.grid_layout.addWidget(self.stacked_widget, 3, 1, 4, 4)
        self.setCentralWidget(self.central_widget)
    
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

    def exit(self):
        app.quit()

    def show_profile(self):
        self.reset_navigation_bar_buttons_checked()
        self.profile = ProfileWidget()
        self.stacked_widget.addWidget(self.profile)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.profile))

    def show_all_devices(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.stacked_widget.all_devices))

    def show_scenes(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.stacked_widget.scenes))

    def show_analytics(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.stacked_widget.analytics))

    def show_schedule(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.stacked_widget.schedule))

    def show_help(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.stacked_widget.help))

    def show_settings(self):
        self.reset_navigation_bar_buttons_checked()
        self.settings = SettingsWidget()
        self.stacked_widget.addWidget(self.settings)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.settings))

    def reset_navigation_bar_buttons_checked(self):
        self.navigation_bar_layout.button_group.setExclusive(False)

        self.navigation_bar_layout.devices_button.setChecked(False)
        self.navigation_bar_layout.scenes_button.setChecked(False)
        self.navigation_bar_layout.analytics_button.setChecked(False)
        self.navigation_bar_layout.schedule_button.setChecked(False)
        self.navigation_bar_layout.help_button.setChecked(False)

        self.navigation_bar_layout.devices_button.update()
        self.navigation_bar_layout.scenes_button.update()
        self.navigation_bar_layout.analytics_button.update()
        self.navigation_bar_layout.schedule_button.update()
        self.navigation_bar_layout.help_button.update()

        self.navigation_bar_layout.button_group.setExclusive(True)


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
