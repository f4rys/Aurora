import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QFrame, QScrollArea, QButtonGroup

from modules.dictionaries.loader import load_dictionary

class SchedulesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

        self.active_buttons_group = QButtonGroup()

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

        self.create_list()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def create_list(self):
        self.clear_layout(self.vlayout)

        if os.path.exists("modules/resources/schedules/schedules.json"):
            with open("modules/resources/schedules/schedules.json", "r", encoding="utf-8") as f:
                schedules = json.load(f)
        else:
            schedules = []

        for schedule in schedules:
            frame = QFrame()
            frame.setFrameShadow(QFrame.Shadow.Plain)
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setProperty("class", "bordered_box")

            schedule_vlayout = QVBoxLayout(frame)

            first_row_layout = QHBoxLayout()
            second_row_layout = QHBoxLayout()

            # First row
            name_label = QLabel(schedule['name'])
            time_label = QLabel(schedule['time'])

            active_button = QPushButton()
            active_button.setProperty("class", "borderless")
            active_button.setObjectName(schedule["id"])
            self.active_buttons_group.addButton(active_button)

            if schedule["active"]:
                active_button.setProperty("state", "on")
            else:
                active_button.setProperty("state", "off")

            self.switch_schedule_state(schedule["id"])

            active_button.clicked.connect(lambda checked, id=schedule["id"]: self.switch_schedule_state(id))

            edit_button = QPushButton()
            edit_button.setProperty("class", "action_bar_button")
            edit_button.setObjectName("edit_button")
            edit_button.clicked.connect(lambda checked, schedule=schedule: self.parent.parent.parent.show_edit_schedule(schedule))

            spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            first_row_layout.addWidget(name_label)
            first_row_layout.addItem(spacer_item)
            first_row_layout.addWidget(time_label)
            first_row_layout.addWidget(active_button)
            first_row_layout.addWidget(edit_button)

            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

            for day in weekdays:
                week_day_label = QLabel()
                if day in schedule['days']:
                    pixmap = QPixmap.fromImage(QImage(self.get_weekday_icon(day, True)))

                    pixmap = pixmap.scaled(25, 25)
                    week_day_label.setPixmap(pixmap)
                else:
                    pixmap = QPixmap.fromImage(QImage(self.get_weekday_icon(day, False)))

                    pixmap = pixmap.scaled(25, 25)
                    week_day_label.setPixmap(pixmap)

                second_row_layout.addWidget(week_day_label)
                second_row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            ###
            schedule_vlayout.addLayout(first_row_layout)
            schedule_vlayout.addLayout(second_row_layout)

            self.vlayout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignTop)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.add_schedule_button = QPushButton("Add schedule")
        self.add_schedule_button.clicked.connect(self.add_schedule)
        self.add_schedule_button.setProperty("class", "device_button")
        self.main_layout.addWidget(self.add_schedule_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def switch_schedule_state(self, button_id):
        active_button = None

        for button in self.active_buttons_group.buttons():
            if button.objectName() == button_id:
                active_button = button

        if active_button is not None:
            if active_button.property("state") == "on":
                active_button.setIcon(QIcon(":/misc/off.png"))
                active_button.setProperty("state", "off")
            elif active_button.property("state") == "off":
                active_button.setIcon(QIcon(":/misc/on.png"))
                active_button.setProperty("state", "on")

    def add_schedule(self):
        empty_schedule =     {
        "id": "",
        "name": "",
        "time": "00:00",
        "days": [],
        "devices": [],
        "dps": "",
        "value": None,
        "active": False
        }

        self.parent.parent.parent.show_edit_schedule(empty_schedule)

    def get_weekday_icon(self, weekday, is_on):
        if weekday == "Monday":
            if is_on:
                return ":/schedule/mon_on.png"
            else:
                return ":/schedule/mon_off.png"
        elif weekday == "Tuesday":
            if is_on:
                return ":/schedule/tue_on.png"
            else:
                return ":/schedule/tue_off.png"
        elif weekday == "Wednesday":
            if is_on:
                return ":/schedule/wed_on.png"
            else:
                return ":/schedule/wed_off.png"
        elif weekday == "Thursday":
            if is_on:
                return ":/schedule/thu_on.png"
            else:
                return ":/schedule/thu_off.png"
        elif weekday == "Friday":
            if is_on:
                return ":/schedule/fri_on.png"
            else:
                return ":/schedule/fri_off.png"
        elif weekday == "Saturday":
            if is_on:
                return ":/schedule/sat_on.png"
            else:
                return ":/schedule/sat_off.png"
        elif weekday == "Sunday":
            if is_on:
                return ":/schedule/sun_on.png"
            else:
                return ":/schedule/sun_off.png"
