import json
import os
from configparser import ConfigParser

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QFrame, QScrollArea

from modules.dictionaries.loader import load_dictionary
from modules.gui.tools import clear_layout
from modules.tuya import TuyaSchedulesManager
from modules.threads import InitiateTuyaSmartModeThread

class SmartModeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setProperty("class", "borderless")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setEnabled(False) # type: ignore
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_widget.setProperty("class", "borderless")
        self.scroll_area.setWidget(self.scroll_widget)

        self.vlayout = QVBoxLayout(self.scroll_widget)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        self.check_settings()

    def check_settings(self):
        clear_layout(self.vlayout)
        self.config = ConfigParser()
        self.config.read('settings.ini')

        mode = self.config.get("General", "smart_mode")

        if mode == 'on':
            self.get_tuya_smart_mode()
        else:
            smart_mode_off_label = QLabel("Smart mode is off")
            self.vlayout.addWidget(smart_mode_off_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def get_tuya_smart_mode(self):
        wait_label = QLabel(self.dictionary["computing_smart_mode"])
        self.vlayout.addWidget(wait_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.thread_worker = InitiateTuyaSmartModeThread()
        self.thread_worker.finished.connect(self.init_ui)
        self.thread_worker.start()

    def init_ui(self, tuya_smart_mode):
        clear_layout(self.vlayout)

        self.tuya_smart_mode = tuya_smart_mode
        self.tuya_schedules_manager = TuyaSchedulesManager("smart_mode")

        if not self.tuya_schedules_manager.schedules:
            empty_list_label = QLabel("No more actions planned for today.")
            self.vlayout.addWidget(empty_list_label, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            for schedule in self.tuya_schedules_manager.schedules:
                frame = QFrame()
                frame.setFrameShadow(QFrame.Shadow.Plain)
                frame.setFrameShape(QFrame.Shape.Box)
                frame.setProperty("class", "bordered_box")

                schedule_vlayout = QVBoxLayout(frame)

                first_row_layout = QHBoxLayout()
                first_row_layout.setObjectName("first_row")

                time_label = QLabel(schedule.time)

                delete_button = QPushButton()
                delete_button.setProperty("class", "action_bar_button")
                delete_button.setObjectName("exit_button")
                delete_button.clicked.connect(lambda checked, schedule=schedule: self.delete_schedule(schedule))

                spacer_item1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                first_row_layout.addItem(spacer_item1)
                first_row_layout.addWidget(time_label)
                first_row_layout.addWidget(delete_button)

                # Actions

                actions_vlayout = QVBoxLayout()

                for function in schedule.functions:

                    action_hlayout = QHBoxLayout()
                    spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                    action_button = QPushButton()
                    value_label = QLabel()

                    if function["code"] == "switch_led":
                        if function["value"]:
                            value_label.setText("Switch: ON")
                        else:
                            value_label.setText("Switch: OFF")
                    elif function["code"] == "bright_value":
                        value_label.setText("Brightness: " + str(int(float(function["value"]["Value"]))))
                    elif function["code"] == "temp_value":
                        value_label.setText("Temperature: " + str(int(float(function["value"]["Value"]))))
                    elif function["code"] == "colour_data":
                        value_label.setText("Colour: " + f"H: {str(int(float(function["value"]["h"]["Value"])))}, S: {str(int(float(function["value"]["s"]["Value"])))}, V: {str(int(float(function["value"]["v"]["Value"])))}")

                    action_button.setObjectName(function["code"])
                    action_button.setProperty("class", "borderless")
                    action_button.setCheckable(True)
                    action_button.setChecked(True)
                    action_button.setDisabled(True)

                    action_hlayout.addWidget(action_button)
                    action_hlayout.addWidget(value_label)
                    action_hlayout.addItem(spacer_item)

                    actions_vlayout.addLayout(action_hlayout)

                # Devices
                devices_layout = QVBoxLayout()
                if os.path.exists("devices.json"):
                    with open("devices.json", "r", encoding="utf-8") as f:
                        devices_data = json.load(f)

                    for device_id in schedule.devices_timers.keys():
                        for device in devices_data:
                            if device["id"] == device_id:
                                device_label = QLabel(device["name"])
                                device_label.setProperty("class", "credentials_input")
                                device_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                                devices_layout.addWidget(device_label)
                                break

                schedule_vlayout.addLayout(first_row_layout)
                schedule_vlayout.addLayout(actions_vlayout)
                schedule_vlayout.addLayout(devices_layout)

                self.vlayout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignTop)

    def delete_schedule(self, schedule):
        schedule.remove_from_cloud()
        self.init_ui(self.tuya_smart_mode)
