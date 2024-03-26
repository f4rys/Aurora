import json
import requests

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem

from modules.tuya import scan_network
from modules.dictionaries.loader import load_dictionary


class AllDevicesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        self.create_list()

        #self.parent = parent

    def open_device(self, device_id):
        #self.parent.show_device(device_id)
        pass

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def create_list(self):

        '''for button in self.findChildren(QPushButton):
            if button != self.refresh_button:
                button.deleteLater()
        for label in self.findChildren(QLabel):
            label.deleteLater()'''

        self.clear_layout(self.vlayout)

        #devices = scan_network()
        devices = []

        self.devices = open('devices.json', encoding="utf-8")
        self.devices_data = json.load(self.devices)
        self.devices.close()

        '''self.device_button = QPushButton("Mock", parent=self)
        self.device_button.setGeometry(QRect(10, 30, 200, 23))
        self.device_button.pressed.connect(lambda: self.parent.setCurrentIndex(0))'''

        for ip in devices:
            self.hlayout = QHBoxLayout()
            self.hlayout.setContentsMargins(0, 0, 0, 0)

            self.device_button = QPushButton(devices[ip]["name"])
            self.device_button.pressed.connect(lambda val=ip: self.open_device(devices[val]["id"]))
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(self.device_button.sizePolicy().hasHeightForWidth())
            self.device_button.setSizePolicy(size_policy)
            self.device_button.setProperty("class", "device_button")

            self.device_icon_label = QLabel()

            matching_nodes = [node for node in self.devices_data if node.get('id') == devices[ip]["id"]]

            icon_value = matching_nodes[0]['icon'] if matching_nodes else None

            image = QImage()
            image.loadFromData(requests.get(str(icon_value), timeout=5).content)
            self.pixmap = QPixmap.fromImage(image)
            self.pixmap = self.pixmap.scaled(23, 23)
            self.device_icon_label.setPixmap(self.pixmap)
            self.device_icon_label.setProperty("class", "device_icon")

            self.hlayout.addWidget(self.device_button)
            self.hlayout.addWidget(self.device_icon_label)
            self.hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.vlayout.addLayout(self.hlayout)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.refresh_button = QPushButton(self.dictionary["refresh"])
        self.refresh_button.clicked.connect(self.create_list)
        self.refresh_button.setProperty("class", "device_button")
        self.vlayout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignBottom)
