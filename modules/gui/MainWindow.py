from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QMetaObject
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QSystemTrayIcon, QFrame

from modules.gui import NavigationBarLayout,MainLayout, ActionBarLayout
from modules.resources import resources
from modules import dictionary


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 300)

        font = QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(9)
        font.setBold(False)
        self.setFont(font)

        self.central_widget = QWidget()

        self.background = QLabel(self.central_widget)
        self.background.setProperty("class", "background")
        self.background.resize(400, 300)

        self.grid_widget = QWidget(self.central_widget)
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

        self.vertical_line = QFrame()
        self.vertical_line.setFrameShape(QFrame.Shape.VLine)
        self.vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.vertical_line.setProperty("class", "vline")
        self.grid_layout.addWidget(self.vertical_line, 2, 1, 5, 1)

        self.action_bar_layout = ActionBarLayout()
        self.action_bar_layout.profile_button.clicked.connect(self.show_profile)
        self.action_bar_layout.settings_button.clicked.connect(self.show_settings)
        self.action_bar_layout.hide_button.clicked.connect(self.hide_window)
        self.action_bar_layout.exit_button.clicked.connect(self.exit)
        self.grid_layout.addLayout(self.action_bar_layout, 2, 1, 1, 10)

        self.main_layout = MainLayout()

        self.grid_layout.addLayout(self.main_layout, 3, 1, 4, 10)
        self.setCentralWidget(self.central_widget)

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
        pass

    def show_all_devices(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.all_devices))
        self.action_bar_layout.set_label(dictionary["devices_title"])

    def show_scenes(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.scenes))
        self.action_bar_layout.set_label(dictionary["scenes_title"])

    def show_analytics(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.analytics))
        self.action_bar_layout.set_label(dictionary["analytics_title"])

    def show_schedule(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.schedule))
        self.action_bar_layout.set_label(dictionary["schedule_title"])

    def show_help(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.help))
        self.action_bar_layout.set_label(dictionary["help_title"])

    def show_settings(self):
        self.reset_navigation_bar_buttons_checked()
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.settings))
        self.action_bar_layout.set_label(dictionary["settings_title"])
        
    def show_profile(self):
        self.reset_navigation_bar_buttons_checked()
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.profile))
        self.action_bar_layout.set_label(dictionary["profile_title"])

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