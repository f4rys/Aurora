from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtGui import QPixmap, QImage
import json
import requests

from modules.tuya import scan_network
from modules import dictionary

class AllDevicesWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.refresh_button = QPushButton(dictionary["refresh"], parent=self)
        self.refresh_button.setGeometry(QRect(10, 0, 200, 23))
        self.refresh_button.clicked.connect(self.create_list)

        self.create_list()

    def open_device(self, device_id):
        self.parent.show_device(device_id)

    def create_list(self):

        for button in self.findChildren(QPushButton):
            if button != self.refresh_button:
                button.deleteLater()
        for label in self.findChildren(QLabel):
            label.deleteLater()

        #devices = scan_network()
        devices = []

        self.devices = open('devices.json')
        self.devices_data = json.load(self.devices)
        self.devices.close()

        self.device_button = QPushButton("Mock", parent=self)
        self.device_button.setGeometry(QRect(10, 30, 200, 23))
        self.device_button.pressed.connect(lambda: self.open_device(self.devices_data[0]["id"]))

        index = 0
   
        for ip in devices:
            index = index + 30
            self.device_button = QPushButton(devices[ip]["name"], parent=self)
            self.device_button.setGeometry(QRect(10, index, 200, 23))
            self.device_button.pressed.connect(lambda val=ip: self.open_device(devices[val]["id"]))

            self.device_icon_label = QLabel(parent=self)
            self.device_icon_label.setGeometry(QRect(220, index, 23, 23))

            matching_nodes = [node for node in self.devices_data if node.get('id') == devices[ip]["id"]]

            icon_value = matching_nodes[0]['icon'] if matching_nodes else None
            
            image = QImage()
            image.loadFromData(requests.get(str(icon_value)).content)
            self.pixmap = QPixmap.fromImage(image)
            self.pixmap = self.pixmap.scaled(23, 23)
            self.device_icon_label.setPixmap(self.pixmap)

            self.device_button.show()
            self.device_icon_label.show()
