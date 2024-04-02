import requests

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from modules.dictionaries.loader import load_dictionary
from modules.tuya import TuyaDevice
from modules.threads import ObtainDevicesThread

class AllDevicesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        self.create_list()

    def open_device(self, device_id):
        self.parent.show_device(device_id)

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
        self.add_refresh_button(self.dictionary["refresh_in_progress"])
        self.refresh_button.setEnabled(False)

        self.thread_worker = ObtainDevicesThread()
        self.thread_worker.finished.connect(self.update_ui)
        self.thread_worker.start()

    def add_refresh_button(self, text):
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.refresh_button = QPushButton(text)
        self.refresh_button.clicked.connect(self.create_list)
        self.refresh_button.setProperty("class", "device_button")
        self.vlayout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def switch(self, device):
        bulb_status = device.is_on()
        if bulb_status is not None:
            if bulb_status:
                device.turn_off()
                self.device_status_button.setIcon(QIcon(":/all_devices/device_off.png"))
            else:
                device.turn_on()
                self.device_status_button.setIcon(QIcon(":/all_devices/device_on.png"))
        else:
            self.device_status_button.setIcon(QIcon(":/all_devices/device_offline.png"))

    def update_ui(self, network_devices, devices_data):
        self.clear_layout(self.vlayout)
        for device in devices_data:
            self.hlayout = QHBoxLayout()
            self.hlayout.setContentsMargins(0, 0, 0, 0)

            self.device_button = QPushButton(device["name"])
            #self.device_button.pressed.connect(lambda val=device_ip: self.open_device(devices[val]["id"]))
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(self.device_button.sizePolicy().hasHeightForWidth())
            self.device_button.setSizePolicy(size_policy)
            self.device_button.setProperty("class", "device_button")

            self.device_icon_label = QLabel()
            self.device_status_button = QPushButton()
            self.device_status_button.setProperty("class", "tab_button")

            device_id = device.get("id")
            bulb_status = None
            
            for ip_address, device_info in network_devices.items():
                if device_info['id'] == device_id:
                    bulb_device = TuyaDevice(device_id)
                    bulb_status = bulb_device.is_on()
                    self.device_status_button.clicked.connect(lambda: self.switch(bulb_device))
                    break
                else:
                    bulb_status = None

            if bulb_status is not None:
                if bulb_status:
                    self.device_status_button.setIcon(QIcon(":/all_devices/device_on.png"))
                else:
                    self.device_status_button.setIcon(QIcon(":/all_devices/device_off.png"))
            else:
                self.device_status_button.setIcon(QIcon(":/all_devices/device_offline.png"))

            image = QImage()
            image.loadFromData(requests.get(str(device["icon"]), timeout=5).content)
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(23, 23)

            self.device_icon_label.setPixmap(pixmap)
            self.device_icon_label.setProperty("class", "device_icon")

            self.hlayout.addWidget(self.device_button)
            self.hlayout.addWidget(self.device_status_button)
            self.hlayout.addWidget(self.device_icon_label)

            self.hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.vlayout.addLayout(self.hlayout)

        self.add_refresh_button(self.dictionary["refresh_completed"])

        self.update()
        self.repaint()
