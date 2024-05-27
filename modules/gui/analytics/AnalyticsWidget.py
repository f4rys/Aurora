import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QScrollArea, QSizePolicy, QPushButton, QSpacerItem, QFrame, QButtonGroup
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from modules.dictionaries import load_dictionary
from modules.gui.tools import clear_layout
from modules.threads import InitiateTuyaAnalyticsThread

class AnalyticsWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 0, 5, 0)

        self.get_tuya_analytics()

    def get_tuya_analytics(self):
        wait_label = QLabel(self.dictionary["computing_analytics"])
        self.main_layout.addWidget(wait_label)

        self.thread_worker = InitiateTuyaAnalyticsThread()
        self.thread_worker.finished.connect(self.init_ui)
        self.thread_worker.start()

    def init_ui(self, tuya_analytics):
        clear_layout(self.main_layout)
        self.tuya_analytics = tuya_analytics

        self.glayout = QGridLayout()
        self.glayout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(self.dictionary["devices_usage"])
        self.title_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.plotlayout = QVBoxLayout()
        self.plotlayout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setProperty("class", "borderless")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setToolTip(self.dictionary["analytics_devices_tooltip"])
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.scroll_widget = QWidget()
        self.scroll_widget.setProperty("class", "borderless")

        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(5, 5, 5, 0)

        self.select_all_button = QPushButton()
        self.select_all_button.setFlat(True)
        self.select_all_button.setProperty("class", "borderless")
        self.select_all_button.setObjectName("select_all")
        self.select_all_button.setToolTip(self.dictionary["select_all_tooltip"])
        self.select_all_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.select_all_button.clicked.connect(self.select_all)

        self.deselect_all_button = QPushButton()
        self.deselect_all_button.setFlat(True)
        self.deselect_all_button.setProperty("class", "borderless")
        self.deselect_all_button.setObjectName("deselect_all")
        self.deselect_all_button.setToolTip(self.dictionary["deselect_all_tooltip"])
        self.deselect_all_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.deselect_all_button.clicked.connect(self.deselect_all)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vertical_line = QFrame()
        self.vertical_line.setFrameShape(QFrame.Shape.VLine)
        self.vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.vertical_line.setProperty("class", "vline")

        self.load_devices()

        self.glayout.addWidget(self.title_label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.glayout.addLayout(self.plotlayout, 1, 0, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.glayout.addWidget(self.scroll_area, 0, 2, 4, 2)
        self.glayout.addWidget(self.select_all_button, 4, 2, 1, 1)
        self.glayout.addWidget(self.deselect_all_button, 4, 3, 1, 1)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addLayout(self.glayout)

        self.select_all()
        self.button_group.buttonClicked.connect(self.update_plot)

    def load_devices(self):
        if os.path.exists("devices.json"):
            with open("devices.json", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = {}

        for device in data:
            label_text = device["name"]
            label_text = ''.join([label_text[i:i+8] + ('\n' if (i + 8) < len(label_text) else '') for i in range(0, len(label_text), 8)])

            button = QPushButton(label_text)
            button.setObjectName(device["id"])
            button.setProperty("class", "device_button")
            button.setCheckable(True)

            self.button_group.addButton(button)
            self.scroll_layout.addWidget(button)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.scroll_layout.addItem(spacer_item)

    def select_all(self):
        for button in self.button_group.buttons():
            button.setChecked(True)
            self.update_plot()

    def deselect_all(self):
        for button in self.button_group.buttons():
            button.setChecked(False)
            self.update_plot()

    def update_plot(self):
        clear_layout(self.plotlayout)

        devices = []
        for button in self.button_group.buttons():
            if button.isChecked():
                devices.append(button.objectName())

        if devices:
            figure = self.tuya_analytics.create_plot(devices)
            if figure is not None:
                plot = FigureCanvasQTAgg(figure)
                plot.setToolTip(self.dictionary["analytics_plot_tooltip"])
                self.plotlayout.addWidget(plot)
            else:
                label = QLabel(self.dictionary["plot_error"])
                self.plotlayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            label = QLabel(self.dictionary["select_device_prompt"])
            self.plotlayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
