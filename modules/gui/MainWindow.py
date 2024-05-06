import os
import json

from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QFrame

from modules.gui import NavigationBarLayout, MainLayout, ActionBarLayout
from modules.tuya import check_credentials
from modules.resources import resources
from modules.dictionaries.loader import load_dictionary


class MainWindow(QMainWindow):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.parent = parent
        self.animation = QPropertyAnimation(self, b"geometry")

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
        self.navigation_bar_layout.schedules_button.clicked.connect(self.show_schedules)
        self.navigation_bar_layout.help_button.clicked.connect(self.show_help)
        self.grid_layout.addLayout(self.navigation_bar_layout, 0, 0, 5, 1)

        self.vertical_line = QFrame()
        self.vertical_line.setFrameShape(QFrame.Shape.VLine)
        self.vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.vertical_line.setProperty("class", "vline")
        self.grid_layout.addWidget(self.vertical_line, 0, 1, 5, 1)

        self.action_bar_layout = ActionBarLayout()
        self.action_bar_layout.profile_button.clicked.connect(self.show_profile)
        self.action_bar_layout.settings_button.clicked.connect(self.show_settings)
        self.action_bar_layout.hide_button.clicked.connect(self.hide_window)
        self.action_bar_layout.exit_button.clicked.connect(self.exit)
        self.grid_layout.addLayout(self.action_bar_layout, 0, 1, 1, 1)

        self.main_layout = MainLayout(self)
        self.grid_layout.addLayout(self.main_layout, 1, 1, 4, 1)
        self.setCentralWidget(self.central_widget)

        if check_credentials():
            self.show_all_devices()
        else:
            self.show_credentials("", "", "", "")

        self.actions()

    def actions(self):
        if os.path.exists("devices.json"):
            with open("devices.json", "r", encoding="utf-8") as f:
                devices = json.load(f)

        if os.path.exists("modules/resources/actions/actions.json"):
            os.remove("modules/resources/actions/actions.json")

        actions = []

        for device in devices:
            device_actions = []
            for action in device.get("mapping").values():
                device_actions.append(action["code"])

            actions.append({
                device["id"] : {
                    "actions" : device_actions
                }
            })

        with open("modules/resources/actions/actions.json", "w", encoding="utf-8") as f:
            json.dump(actions, f, indent=2)

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
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(x + window_width//2, y + window_height//2, 0, 0))
            self.animation.setEndValue(QRect(x, y, window_width, window_height))

            self.animation.start()

    def exit(self):
        self.parent.exit()

    def restart(self):
        self.parent.restart_window()

    def show_edit_schedule(self, schedule):
        self.main_layout.stacked_widget.edit_schedule.init_ui(schedule)
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.edit_schedule))
        self.action_bar_layout.set_label("Add/edit schedule")

    def show_device(self, device):
        self.reset_navigation_bar_buttons_checked()
        self.main_layout.stacked_widget.device.init_ui(device)
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.device))
        self.action_bar_layout.set_label(device.name)

    def show_all_devices(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.all_devices))
        self.action_bar_layout.set_label(self.dictionary["devices_title"])

    def show_scenes(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.scenes))
        self.action_bar_layout.set_label(self.dictionary["scenes_title"])

    def show_analytics(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.analytics))
        self.action_bar_layout.set_label(self.dictionary["analytics_title"])

    def show_schedules(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.schedules))
        self.action_bar_layout.set_label(self.dictionary["schedules_title"])

    def show_help(self):
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.help))
        self.action_bar_layout.set_label(self.dictionary["help_title"])

    def show_settings(self):
        self.reset_navigation_bar_buttons_checked()
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.settings))
        self.action_bar_layout.set_label(self.dictionary["settings_title"])

    def show_profile(self):
        self.reset_navigation_bar_buttons_checked()
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.profile))
        self.action_bar_layout.set_label(self.dictionary["profile_title"])

    def show_credentials(self, api_key, api_secret, api_region, api_device_id):
        self.reset_navigation_bar_buttons_checked()
        self.disable_buttons()
        self.main_layout.stacked_widget.credentials.set_credentials(api_key, api_secret, api_device_id, api_region)
        self.main_layout.stacked_widget.setCurrentIndex(self.main_layout.stacked_widget.indexOf(self.main_layout.stacked_widget.credentials))
        self.action_bar_layout.set_label(self.dictionary["credentials_title"])

    def disable_buttons(self):
        self.navigation_bar_layout.devices_button.setEnabled(False)
        self.navigation_bar_layout.scenes_button.setEnabled(False)
        self.navigation_bar_layout.analytics_button.setEnabled(False)
        self.navigation_bar_layout.schedules_button.setEnabled(False)
        self.navigation_bar_layout.help_button.setEnabled(False)
        self.action_bar_layout.profile_button.setEnabled(False)
        self.action_bar_layout.settings_button.setEnabled(False)

    def enable_buttons(self):
        self.navigation_bar_layout.devices_button.setEnabled(True)
        self.navigation_bar_layout.scenes_button.setEnabled(True)
        self.navigation_bar_layout.analytics_button.setEnabled(True)
        self.navigation_bar_layout.schedules_button.setEnabled(True)
        self.navigation_bar_layout.help_button.setEnabled(True)
        self.action_bar_layout.profile_button.setEnabled(True)
        self.action_bar_layout.settings_button.setEnabled(True)

    def reset_navigation_bar_buttons_checked(self):
        self.navigation_bar_layout.button_group.setExclusive(False)

        self.navigation_bar_layout.devices_button.setChecked(False)
        self.navigation_bar_layout.scenes_button.setChecked(False)
        self.navigation_bar_layout.analytics_button.setChecked(False)
        self.navigation_bar_layout.schedules_button.setChecked(False)
        self.navigation_bar_layout.help_button.setChecked(False)

        self.navigation_bar_layout.devices_button.update()
        self.navigation_bar_layout.scenes_button.update()
        self.navigation_bar_layout.analytics_button.update()
        self.navigation_bar_layout.schedules_button.update()
        self.navigation_bar_layout.help_button.update()

        self.navigation_bar_layout.button_group.setExclusive(True)
