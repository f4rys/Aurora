import requests

from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QScrollArea

from modules.dictionaries.loader import load_dictionary
from modules.threads import InitiateTuyaManagerThread

from modules.gui.tools import clear_layout

class AllDevicesWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
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

        self.create_list()

    def open_device(self, device):
        self.parent.parent.parent.show_device(device)

    def create_list(self):
        clear_layout(self.vlayout)
        self.delete_reload_button()

        self.add_reload_button(self.dictionary["reload_in_progress"])
        self.reload_button.setEnabled(False)

        self.thread_worker = InitiateTuyaManagerThread()
        self.thread_worker.finished.connect(self.update_ui)
        self.thread_worker.start()

    def add_reload_button(self, text):
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.reload_button = QPushButton(text)
        self.reload_button.clicked.connect(self.create_list)
        self.reload_button.setProperty("class", "device_button")
        self.reload_button.setObjectName("reload_button")
        self.main_layout.addWidget(self.reload_button, alignment=Qt.AlignmentFlag.AlignBottom)

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
        except Exception:
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

        try:
            image = QImage()
            image.loadFromData(requests.get(str(icon_link), timeout=5).content)
            pixmap = QPixmap.fromImage(image)
        except requests.exceptions.ConnectionError:
            pixmap = QPixmap(":/all_devices/bulb_icon_error.png")

        pixmap = pixmap.scaled(23, 23)

        device_icon_label.setPixmap(pixmap)
        device_icon_label.setProperty("class", "device_icon")

        hlayout.addWidget(device_button)
        hlayout.addWidget(device_status_button)
        hlayout.addWidget(device_icon_label)

        hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return hlayout

    def update_ui(self, manager):
        clear_layout(self.vlayout)
        self.delete_reload_button()

        self.manager = manager

        for device in self.manager.active_devices.values():
            hlayout = self.add_device_button(device.name, device.icon_link, device)
            self.vlayout.addLayout(hlayout)

        for device in self.manager.inactive_devices.values():
            hlayout = self.add_device_button(device["name"], device.get("icon_link"), None)
            self.vlayout.addLayout(hlayout)

        self.add_reload_button(self.dictionary["reload_completed"])

        self.update()
        self.repaint()

    def delete_reload_button(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QObject) and widget.objectName() == "reload_button":
                    self.main_layout.removeItem(item)
                    widget.deleteLater()
                    break
