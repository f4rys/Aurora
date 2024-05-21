import json
import os

from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QScrollArea, QButtonGroup, QLineEdit, QTimeEdit
from tzlocal import get_localzone

from modules.dictionaries.loader import load_dictionary
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab
from modules.gui.tools import clear_layout, show_error_toast
from modules.tuya import TuyaSchedule

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

    def init_ui(self, schedule, new):
        clear_layout(self.vlayout)

        self.new = new
        self.schedule = schedule

        self.name_edit_label = QLabel(self.dictionary["set_schedule_name"])
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.schedule.alias_name)
        self.name_edit.setProperty("class", "credentials_input")

        self.time_edit_label = QLabel(self.dictionary["set_schedule_time"])
        self.time_edit = QTimeEdit()
        self.time_edit.setTimeRange(QTime(0, 0, 0), QTime(23, 59, 59))
        self.set_time()

        self.weekdays_label = QLabel(self.dictionary["set_schedule_weekdays"])
        self.weekdays_hlayout = QHBoxLayout()
        self.weekdays_hlayout.setSpacing(0)
        self.load_weekdays()

        self.devices_label = QLabel(self.dictionary["select_schedule_devices"])
        self.load_devices()

        self.action_label = QLabel(self.dictionary["select_schedule_action"])
        self.actions_hlayout = QHBoxLayout()
        if self.schedule.devices_timers != {}:
            self.create_actions_list()

        self.value_label = QLabel(self.dictionary["enter_action_value"])
        self.value_vlayout = QVBoxLayout()
        if self.schedule.devices_timers != {}:
            self.create_value_layout()

        self.save_button = QPushButton(self.dictionary["save_schedule_changes"])
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

        ranges = self.get_ranges()

        action = self.actions_group.button(self.actions_group.checkedId())
        if action is not None:
            action = action.objectName()

            if action == "switch_led":
                self.value_label.setText(self.dictionary["select_switch_value"])
                value_layout = QHBoxLayout()
                value_layout.setContentsMargins(0, 0, 0, 0)

                on_button = QPushButton(self.dictionary["on"])
                off_button = QPushButton(self.dictionary["off"])

                on_button.setProperty("class", "device_button")
                off_button.setProperty("class", "device_button")

                on_button.setObjectName("ON")
                off_button.setObjectName("OFF")

                on_button.setCheckable(True)
                off_button.setCheckable(True)

                try:
                    if self.schedule.functions[0]["value"]:
                        on_button.setChecked(True)
                    else:
                        off_button.setChecked(True)
                except Exception:
                    pass

                self.switch_button_group.addButton(on_button)
                self.switch_button_group.addButton(off_button)

                value_layout.addWidget(on_button)
                value_layout.addWidget(off_button)

                self.value_vlayout.addLayout(value_layout)
            elif action == "bright_value":
                self.value_label.setText(self.dictionary["select_brightness_value"])
                self.value_widget = WhiteModeTab()

                self.value_widget.brightness_slider.setRange(max(ranges["brightness"]["min"]), min(ranges["brightness"]["max"]))
                self.value_widget.temperature_slider.setRange(max(ranges["temperature"]["min"]), min(ranges["temperature"]["max"]))

                try:
                    self.value_widget.brightness_slider.setValue(int(float(self.schedule.functions[0]["value"]["Value"])))
                    self.value_widget.temperature_slider.setValue(int(float(self.schedule.functions[1]["value"]["Value"])))
                except Exception:
                    self.value_widget.brightness_slider.setValue(0)
                    self.value_widget.temperature_slider.setValue(0)

                self.value_vlayout.addWidget(self.value_widget)
            elif action == "colour_data":
                self.value_label.setText(self.dictionary["select_colour_value"])
                self.value_widget = ColourModeTab()

                self.value_widget.hue_slider.setRange(max(ranges["h"]["min"]), min(ranges["h"]["max"]))
                self.value_widget.value_slider.setRange(max(ranges["s"]["min"]), min(ranges["s"]["max"]))
                self.value_widget.saturation_slider.setRange(max(ranges["v"]["min"]), min(ranges["v"]["max"]))

                try:
                    self.value_widget.hue_slider.setValue(int(float(self.schedule.functions[0]["value"]["h"]["Value"])))
                    self.value_widget.value_slider.setValue(int(float(self.schedule.functions[0]["value"]["s"]["Value"])))
                    self.value_widget.saturation_slider.setValue(int(float(self.schedule.functions[0]["value"]["v"]["Value"])))
                except Exception:
                    self.value_widget.hue_slider.setValue(0)
                    self.value_widget.value_slider.setValue(0)
                    self.value_widget.saturation_slider.setValue(0)

                self.value_vlayout.addWidget(self.value_widget)

    def set_time(self):
        hours, minutes = map(int, self.schedule.time.split(":"))
        self.time_edit.setTime(QTime(hours, minutes))

    def load_available_actions(self, ids):
        if os.path.exists("modules/resources/json/actions.json"):
            with open("modules/resources/json/actions.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            try:
                filtered_data = [node for node in data if list(node.keys())[0] in ids]
                actions_sets = [set(list(node.values())[0]["actions"]) for node in filtered_data]
                common_actions = set.intersection(*actions_sets)
                common_actions = list(common_actions)

                return common_actions

            except TypeError:
                return []
        else:
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
            warning_label = QLabel(self.dictionary["select_device_prompt"])
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
                    if self.schedule.functions != []:
                        if self.schedule.functions[0]["code"] == "switch_led" and action_button:
                            action_button.setChecked(True)
                elif action == "bright_value_v2":
                    action_button = QPushButton()
                    action_button.setProperty("class", "weekday_button")
                    action_button.setCheckable(True)
                    action_button.setObjectName("bright_value")
                    action_button.setMinimumSize(25, 25)
                    action_button.clicked.connect(self.create_value_layout)
                    self.actions_group.addButton(action_button)
                    self.actions_hlayout.addWidget(action_button)
                    if self.schedule.functions != []:
                        if self.schedule.functions[0]["code"] == "bright_value" and action_button:
                            action_button.setChecked(True)
                elif action == "colour_data_v2":
                    action_button = QPushButton()
                    action_button.setProperty("class", "weekday_button")
                    action_button.setCheckable(True)
                    action_button.setObjectName("colour_data")
                    action_button.setMinimumSize(25, 25)
                    action_button.clicked.connect(self.create_value_layout)
                    self.actions_group.addButton(action_button)
                    self.actions_hlayout.addWidget(action_button)
                    if self.schedule.functions != []:
                        if self.schedule.functions[0]["code"] == "colour_data" and action_button:
                            action_button.setChecked(True)

        self.actions_hlayout.addItem(spacer)

    def load_weekdays(self):
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for i, day in enumerate(weekdays):
            week_day_button = QPushButton()
            week_day_button.setObjectName(day)
            week_day_button.setProperty("class", "weekday_button")
            week_day_button.setCheckable(True)
            state = self.schedule.loops[i] == "1"
            if state:
                week_day_button.setChecked(True)
            else:
                week_day_button.setChecked(False)

            self.weekdays_group.addButton(week_day_button)
            self.weekdays_hlayout.addWidget(week_day_button)

    def load_devices(self):
        self.devices_vlayout = QVBoxLayout()
        if os.path.exists("devices.json"):
            with open("devices.json", encoding="utf-8") as file:
                data = json.load(file)

            for device in data:
                button = QPushButton(device["name"])
                button.setObjectName(device["id"])
                button.setProperty("class", "device_button")
                button.setCheckable(True)
                button.clicked.connect(self.create_actions_list)
                self.devices_group.addButton(button)
                if device["id"] in self.schedule.devices_timers.keys():
                    button.setChecked(True)
                self.devices_vlayout.addWidget(button)

    def weekarray_to_string(self, weekarray):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        weekday_dict = {day: 0 for day in days}
        for day in weekarray:
            weekday_dict[day] = 1
        return ''.join(str(weekday_dict[day]) for day in days)

    def get_ranges(self):
        ids = []

        results = {
                "brightness": {"min": [], "max": []},
                "temperature": {"min": [], "max": []},
                "h": {"min": [], "max": []},
                "s": {"min": [], "max": []},
                "v": {"min": [], "max": []},
            }

        for button in self.devices_group.buttons():
            if button.isChecked():
                ids.append(button.objectName())

        if os.path.exists("devices.json"):
            with open("devices.json", encoding="utf-8") as file:
                data = json.load(file)

            for device in data:
                if device["id"] in ids:
                    mapping = device["mapping"]
                    results["brightness"]["min"].append(mapping["22"]["values"]["min"])
                    results["brightness"]["max"].append(mapping["22"]["values"]["max"])
                    results["temperature"]["min"].append(mapping["23"]["values"]["min"])
                    results["temperature"]["max"].append(mapping["23"]["values"]["max"])

                    if "24" in mapping:
                        results["h"]["min"].append(mapping["24"]["values"]["h"]["min"])
                        results["h"]["max"].append(mapping["24"]["values"]["h"]["max"])
                        results["s"]["min"].append(mapping["24"]["values"]["s"]["min"])
                        results["s"]["max"].append(mapping["24"]["values"]["s"]["max"])
                        results["v"]["min"].append(mapping["24"]["values"]["v"]["min"])
                        results["v"]["max"].append(mapping["24"]["values"]["v"]["max"])

        return results

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

        new_devices = []
        for button in self.devices_group.buttons():
            if button.isChecked():
                new_devices.append(button.objectName())

        action = ""
        action_button = self.actions_group.checkedButton()
        if action_button:
            action = action_button.objectName()

        value = ""
        functions = []
        if action == "switch_led":
            checked_button = self.switch_button_group.checkedButton()
            if checked_button:
                button_name = checked_button.objectName()
                if button_name == "ON":
                    value = True
                elif button_name == "OFF":
                    value = False
            functions.append({"code": action, "value": value})
        elif action == "bright_value":
            if isinstance(self.value_widget, WhiteModeTab):
                brightness = self.value_widget.brightness_slider.value()
                temperature = self.value_widget.temperature_slider.value()
                functions.append({"code": "bright_value", "value": brightness})
                functions.append({"code": "temp_value", "value": temperature})
        elif action == "colour_data":
            if isinstance(self.value_widget, ColourModeTab):
                h = self.value_widget.hue_slider.value()
                s = self.value_widget.saturation_slider.value()
                v = self.value_widget.value_slider.value()
                functions.append({"code": "colour_data", "value": {"h": h, "s": s, "v": v}})

        if self.new:
            devices = dict.fromkeys(new_devices, "")
            schedule = TuyaSchedule(alias_name=schedule_name, enable=True, time=time, timezone_id=user_timezone, loops=weekdays_string, devices_timers=devices, functions=functions)
            responses = schedule.save_to_cloud()
            if False in responses:
                show_error_toast(self)
        else:
            old_devices = set(self.schedule.devices_timers.keys())
            new_devices = set(new_devices)

            # Items only in the first list
            only_in_list1 = old_devices - new_devices
            for item in only_in_list1:
                devices = {item: self.schedule.devices_timers[item]}
                schedule = TuyaSchedule(alias_name=schedule_name, enable=True, time=time, timezone_id=user_timezone, loops=weekdays_string, devices_timers=devices, functions=functions)
                responses = schedule.remove_from_cloud()
                if False in responses:
                    show_error_toast(self)

            # Items only in the second list
            only_in_list2 = new_devices - old_devices
            for item in only_in_list2:
                devices = {item: ""}
                schedule = TuyaSchedule(alias_name=schedule_name, enable=True, time=time, timezone_id=user_timezone, loops=weekdays_string, devices_timers=devices, functions=functions)
                responses = schedule.save_to_cloud()
                if False in responses:
                    show_error_toast(self)

            # Items in both lists
            in_both_lists = old_devices & new_devices
            for item in in_both_lists:
                devices = {item: self.schedule.devices_timers[item]}
                schedule = TuyaSchedule(alias_name=schedule_name, enable=True, time=time, timezone_id=user_timezone, loops=weekdays_string, devices_timers=devices, functions=functions)
                responses = schedule.modify_on_cloud()
                if False in responses:
                    show_error_toast(self)

        self.parent.parent.parent.show_schedules()
