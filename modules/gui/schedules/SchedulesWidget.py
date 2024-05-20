import json
import os

from PyQt6.QtCore import Qt, QObject
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QFrame, QScrollArea

from modules.dictionaries.loader import load_dictionary
from modules.gui.tools import clear_layout, show_error_toast
from modules.threads import InitiateTuyaSchedulesManagerThread

class SchedulesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

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

    def create_list(self):
        clear_layout(self.vlayout)
        self.delete_add_schedule_button()

        self.append_add_schedule_button(self.dictionary["reloading_schedules"])
        self.add_schedule_button.setEnabled(False)

        self.thread_worker = InitiateTuyaSchedulesManagerThread()
        self.thread_worker.finished.connect(self.update_ui)
        self.thread_worker.start()

    def append_add_schedule_button(self, text):
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.add_schedule_button = QPushButton(text)
        self.add_schedule_button.clicked.connect(self.add_schedule)
        self.add_schedule_button.setProperty("class", "device_button")
        self.add_schedule_button.setObjectName("add_schedule_button")
        self.main_layout.addWidget(self.add_schedule_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def update_ui(self, manager):
        clear_layout(self.vlayout)
        self.delete_add_schedule_button()

        self.schedules_manager = manager

        for schedule in self.schedules_manager.schedules:
            frame = QFrame()
            frame.setFrameShadow(QFrame.Shadow.Plain)
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setProperty("class", "bordered_box")

            schedule_vlayout = QVBoxLayout(frame)

            first_row_layout = QHBoxLayout()
            first_row_layout.setObjectName("first_row")
            second_row_layout = QHBoxLayout()
            second_row_layout.setObjectName("second_row")
            third_row_layout = QHBoxLayout()
            second_row_layout.setObjectName("third_row")

            # First row
            name_label = QLabel(schedule.alias_name)

            # Second row
            time_label = QLabel(schedule.time)

            action_button = QPushButton()
            if schedule.functions[0]["code"] == "switch_led":
                if schedule.functions[0]["value"]:
                    action_button.setObjectName("switch_led_on")
                else:
                    action_button.setObjectName("switch_led_off")
            else:
                action_button.setObjectName(schedule.functions[0]["code"])

            action_button.setProperty("class", "borderless")
            action_button.setCheckable(True)
            action_button.setChecked(True)
            action_button.setDisabled(True)

            active_button = QPushButton()
            active_button.setProperty("class", "borderless")
            active_button.setObjectName("active_button")
            active_button.setCheckable(True)

            if schedule.enable:
                active_button.setChecked(True)

            active_button.clicked.connect(lambda checked, schedule=schedule, button=active_button: self.switch_schedule_state(button, schedule))

            edit_button = QPushButton()
            edit_button.setProperty("class", "action_bar_button")
            edit_button.setObjectName("edit_button")
            edit_button.clicked.connect(lambda checked, schedule=schedule: self.parent.parent.parent.show_edit_schedule(schedule, False))

            delete_button = QPushButton()
            delete_button.setProperty("class", "action_bar_button")
            delete_button.setObjectName("exit_button")
            delete_button.clicked.connect(lambda checked, schedule=schedule: self.delete_schedule(schedule))

            spacer_item1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            spacer_item2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            first_row_layout.addWidget(name_label)
            first_row_layout.addItem(spacer_item1)

            second_row_layout.addItem(spacer_item2)
            second_row_layout.addWidget(time_label)
            second_row_layout.addWidget(action_button)
            second_row_layout.addWidget(active_button)
            second_row_layout.addWidget(edit_button)
            second_row_layout.addWidget(delete_button)

            # Third row
            weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

            for i, day in enumerate(weekdays):
                week_day_label = QPushButton()
                week_day_label.setObjectName(day)
                week_day_label.setDisabled(True)
                week_day_label.setProperty("class", "weekday_button")
                week_day_label.setCheckable(True)
                state = schedule.loops[i] == "1"
                if state:
                    week_day_label.setChecked(True)
                else:
                    week_day_label.setChecked(False)

                third_row_layout.addWidget(week_day_label)
                third_row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Devices
            devices_layout = QVBoxLayout()
            if os.path.exists("devices.json"):
                with open("devices.json", "r") as f:
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
            schedule_vlayout.addLayout(second_row_layout)
            schedule_vlayout.addLayout(third_row_layout)
            schedule_vlayout.addLayout(devices_layout)

            self.vlayout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignTop)

        self.append_add_schedule_button(self.dictionary["add_schedule"])

    def switch_schedule_state(self, button, schedule):
        if isinstance(button, QPushButton):

            if button.isChecked():
                value = True
            else:
                value = False
            responses = schedule.change_state_on_cloud(value)
            if False in responses:
                button.setChecked(not value)
                show_error_toast(self)

    def add_schedule(self):
        self.parent.parent.parent.show_edit_schedule(self.schedules_manager.empty_schedule, True)

    def delete_schedule(self, schedule):
        responses = schedule.remove_from_cloud()
        if False in responses:
            show_error_toast(self)
        self.create_list()

    def delete_add_schedule_button(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QObject) and widget.objectName() == "add_schedule_button":
                    self.main_layout.removeItem(item)
                    widget.deleteLater()
                    break
