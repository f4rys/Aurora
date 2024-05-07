import json

from PyQt6.QtCore import QTime, QSize
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QScrollArea, QButtonGroup, QLineEdit, QTimeEdit
from tzlocal import get_localzone

from modules.dictionaries.loader import load_dictionary
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab
from modules.gui.tools import clear_layout

class EditScheduleWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

        self.actions_group = QButtonGroup()
        self.weekdays_group = QButtonGroup()
        self.weekdays_group.setExclusive(False)
        self.devices_group = QButtonGroup()
        self.devices_group.setExclusive(False)

        self.switch_button_group = QButtonGroup()
        self.switch_button_group.setExclusive(True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setProperty("class", "borderless")
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_widget.setProperty("class", "borderless")
        self.scroll_area.setWidget(self.scroll_widget)

        self.vlayout = QVBoxLayout(self.scroll_widget)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

    def init_ui(self, schedule):
        clear_layout(self.vlayout)

        self.schedule = schedule

        self.name_edit_label = QLabel("1. Set schedule name:")
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.schedule["name"])
        self.name_edit.setProperty("class", "credentials_input")

        self.time_edit_label = QLabel("2. Set time:")
        self.time_edit = QTimeEdit()
        self.time_edit.setTimeRange(QTime(0, 0, 0), QTime(23, 59, 59))
        self.set_time(self.schedule)

        self.weekdays_label = QLabel("3. Select weekdays:")
        self.weekdays_hlayout = QHBoxLayout()
        self.weekdays_hlayout.setSpacing(0)
        self.load_weekdays(self.schedule)

        self.devices_label = QLabel("4. Select devices:")
        self.load_devices(self.schedule)

        self.action_label = QLabel("5. Select action:")
        self.actions_hlayout = QHBoxLayout()
        self.create_actions_list()

        self.value_label = QLabel("6. Enter value:")
        self.value_vlayout = QVBoxLayout()
        self.create_value_layout()

        self.save_button = QPushButton("Save changes")
        self.save_button.setProperty("class", "device_button")
        self.save_button.clicked.connect(self.save_changes)

        self.vlayout.addWidget(self.name_edit_label)
        self.vlayout.addWidget(self.name_edit)
        self.vlayout.addWidget(self.time_edit_label)
        self.vlayout.addWidget(self.time_edit)
        self.vlayout.addWidget(self.weekdays_label)
        self.vlayout.addLayout(self.weekdays_hlayout)
        self.vlayout.addWidget(self.devices_label)
        self.vlayout.addLayout(self.devices_vlayout)
        self.vlayout.addWidget(self.action_label)
        self.vlayout.addLayout(self.actions_hlayout)
        self.vlayout.addWidget(self.value_label)
        self.vlayout.addLayout(self.value_vlayout)
        self.vlayout.addWidget(self.save_button)

    def create_value_layout(self):
        clear_layout(self.value_vlayout)

        action = self.actions_group.button(self.actions_group.checkedId())
        if action is not None:
            action = action.objectName()

            if action == "switch_led":
                self.value_label.setText("6. Enter value for ON/OFF:")
                value_layout = QHBoxLayout()
                value_layout.setContentsMargins(0, 0, 0, 0)

                on_button = QPushButton("On")
                off_button = QPushButton("Off")

                on_button.setProperty("class", "device_button")
                off_button.setProperty("class", "device_button")

                on_button.setObjectName("ON")
                off_button.setObjectName("OFF")

                on_button.setCheckable(True)
                off_button.setCheckable(True)

                self.switch_button_group.addButton(on_button)
                self.switch_button_group.addButton(off_button)

                value_layout.addWidget(on_button)
                value_layout.addWidget(off_button)

                self.value_vlayout.addLayout(value_layout)
            elif action == "bright_value_v2":
                self.value_label.setText("6. Enter values for brightness and temperature:")
                self.value_widget = WhiteModeTab()
                self.value_vlayout.addWidget(self.value_widget)
            elif action == "colour_data_v2":
                self.value_label.setText("6. Enter values for colour and brightness:")
                self.value_widget = ColourModeTab()
                self.value_vlayout.addWidget(self.value_widget)

    def set_time(self, schedule):
        hours, minutes = map(int, schedule["time"].split(":"))
        self.time_edit.setTime(QTime(hours, minutes))

    def load_available_actions(self, ids):
        with open("modules/resources/actions/actions.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            filtered_data = [node for node in data if list(node.keys())[0] in ids]
            actions_sets = [set(list(node.values())[0]["actions"]) for node in filtered_data]
            common_actions = set.intersection(*actions_sets)
            common_actions = list(common_actions)

            return common_actions

        except TypeError:
            return []

    def create_actions_list(self):
        clear_layout(self.actions_hlayout)

        ids = []

        for button in self.devices_group.buttons():
            if button.isChecked():
                ids.append(button.objectName())

        common_actions = self.load_available_actions(ids)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        if not common_actions:
            warning_label = QLabel("Select at least one device")
            self.actions_hlayout.addWidget(warning_label)
        else:
            for action in common_actions:
                if action == "switch_led":
                    action_button = QPushButton()
                    action_button.setProperty("class", "weekday_button")
                    action_button.setCheckable(True)
                    action_button.setObjectName(action)
                    action_button.setMinimumSize(25, 25)
                    action_button.clicked.connect(self.create_value_layout)
                    self.actions_group.addButton(action_button)
                    self.actions_hlayout.addWidget(action_button)
                elif action == "bright_value_v2":
                    action_button = QPushButton()
                    action_button.setProperty("class", "weekday_button")
                    action_button.setCheckable(True)
                    action_button.setObjectName(action)
                    action_button.setMinimumSize(25, 25)
                    action_button.clicked.connect(self.create_value_layout)
                    self.actions_group.addButton(action_button)
                    self.actions_hlayout.addWidget(action_button)
                elif action == "colour_data_v2":
                    action_button = QPushButton()
                    action_button.setProperty("class", "weekday_button")
                    action_button.setCheckable(True)
                    action_button.setObjectName(action)
                    action_button.setMinimumSize(25, 25)
                    action_button.clicked.connect(self.create_value_layout)
                    self.actions_group.addButton(action_button)
                    self.actions_hlayout.addWidget(action_button)

        self.actions_hlayout.addItem(spacer)

    def load_weekdays(self, schedule):
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            week_day_button = QPushButton()
            week_day_button.setProperty("class", "weekday_button")
            week_day_button.setObjectName(day)
            week_day_button.setCheckable(True)
            week_day_button.setIconSize(QSize(27, 27))

            if day in schedule['days']:
                week_day_button.setChecked(True)
            else:
                week_day_button.setChecked(False)

            self.weekdays_group.addButton(week_day_button)
            self.weekdays_hlayout.addWidget(week_day_button)

    def load_devices(self, schedule):
        self.devices_vlayout = QVBoxLayout()

        with open("devices.json", encoding="utf-8") as file:
            data = json.load(file)

        for device in data:
            button = QPushButton(device["name"])
            button.setObjectName(device["id"])
            button.setProperty("class", "device_button")
            button.setCheckable(True)
            button.clicked.connect(self.create_actions_list)
            self.devices_group.addButton(button)
            if device["id"] in schedule["devices"]:
                button.setChecked(True)

            self.devices_vlayout.addWidget(button)

    def weekarray_to_string(self, weekarray):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekday_dict = {day: 0 for day in days}
        for day in weekarray:
            weekday_dict[day] = 1
        return ''.join(str(weekday_dict[day]) for day in days)

    def save_changes(self):
        schedule_name = self.name_edit.text()

        qtime = self.time_edit.time()
        time = f"{qtime.hour():02d}:{qtime.minute():02d}"
        user_timezone = str(get_localzone())

        weekdays = []
        for button in self.weekdays_group.buttons():
            if button.isChecked():
                weekdays.append(button.objectName())

        weekdays_string = self.weekarray_to_string(weekdays)

        devices = []
        for button in self.devices_group.buttons():
            if button.isChecked():
                devices.append(button.objectName())

        action = ""
        action_button = self.actions_group.checkedButton()
        if action_button:
            action = action_button.objectName()

        value = ""
        if action == "switch_led":
            checked_button = self.switch_button_group.checkedButton()
            if checked_button:
                button_name = checked_button.objectName()
                if button_name == "ON":
                    value = True
                elif button_name == "OFF":
                    value = False
        elif action == "bright_value_v2":
            if hasattr(self.value_widget, "brightness_slider") and hasattr(self.value_widget, "temperature_slider"):
                brightness = self.value_widget.brightness_slider.value()
                temperature = self.value_widget.temperature_slider.value()
                value = {
                    "brightness": brightness,
                    "temperature": temperature
                }

        elif action == "colour_data_v2":
            if hasattr(self.value_widget, "hue_slider") and hasattr(self.value_widget, "saturation_slider") and hasattr(self.value_widget, "value_slider"):
                h = self.value_widget.hue_slider.value()
                s = self.value_widget.saturation_slider.value()
                v = self.value_widget.value_slider.value()
                value = {
                    "h": h,
                    "s": s,
                    "v": v
                }

        print(self.schedule["id"], schedule_name, time, user_timezone, weekdays_string, devices, action, value)
