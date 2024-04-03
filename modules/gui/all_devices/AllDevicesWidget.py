import requests

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from modules.dictionaries.loader import load_dictionary
from modules.threads import InitiateTuyaManagerThread

class AllDevicesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        self.create_list()

    def open_device(self, device):
        self.parent.parent.parent.show_device(device)

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

        self.thread_worker = InitiateTuyaManagerThread()
        self.thread_worker.finished.connect(self.update_ui)
        self.thread_worker.start()

    def add_refresh_button(self, text):
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.refresh_button = QPushButton(text)
        self.refresh_button.clicked.connect(self.create_list)
        self.refresh_button.setProperty("class", "device_button")
        self.vlayout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def switch(self, device, state, device_status_button, device_button):
        if state:
            device.turn_on()
        else:
            device.turn_off()

        self.set_icon_and_action(device_status_button, device_button, device)

    def set_icon_and_action(self, device_status_button, device_button, device):
        try:
            device_status_button.clicked.disconnect()
            device_button.clicked.disconnect()
        except Exception as e:
            pass

        if device is not None:
            device_button.clicked.connect(lambda: self.open_device(device))
            status = device.is_on()
            if status:
                device_status_button.setIcon(QIcon(":/all_devices/device_on.png"))
                device_status_button.clicked.connect(lambda: self.switch(device, False, device_status_button, device_button))
            else:
                device_status_button.setIcon(QIcon(":/all_devices/device_off.png"))
                device_status_button.clicked.connect(lambda: self.switch(device, True, device_status_button, device_button))
        else:
            device_status_button.setIcon(QIcon(":/all_devices/device_offline.png"))
            device_button.setEnabled(False)

    def add_device_button(self, name, icon_link, device):
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)

        device_button = QPushButton(name)
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(device_button.sizePolicy().hasHeightForWidth())
        device_button.setSizePolicy(size_policy)
        device_button.setProperty("class", "device_button")

        device_icon_label = QLabel()
        device_status_button = QPushButton()
        device_status_button.setProperty("class", "tab_button")

        self.set_icon_and_action(device_status_button, device_button, device)

        image = QImage()
        image.loadFromData(requests.get(str(icon_link), timeout=5).content)
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(23, 23)

        device_icon_label.setPixmap(pixmap)
        device_icon_label.setProperty("class", "device_icon")

        hlayout.addWidget(device_button)
        hlayout.addWidget(device_status_button)
        hlayout.addWidget(device_icon_label)

        hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return hlayout

    def update_ui(self, manager):
        self.clear_layout(self.vlayout)

        self.manager = manager

        for dev_id, device in self.manager.active_devices.items():
            hlayout = self.add_device_button(device.name, device.icon_link, device)
            self.vlayout.addLayout(hlayout)

        for dev_id, device in self.manager.inactive_devices.items():
            hlayout = self.add_device_button(device["name"], device.get("icon_link"), None)
            self.vlayout.addLayout(hlayout)

        self.add_refresh_button(self.dictionary["refresh_completed"])

        self.update()
        self.repaint()
