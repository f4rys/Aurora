import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QGridLayout, QSpacerItem

from modules.dictionaries.loader import load_dictionary

class ProfileWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(10, 10, 10, 0)

        self.glayout = QGridLayout()
        self.glayout.setContentsMargins(0, 0, 0, 0)

        self.api_key, self.api_secret, self.api_region, self.api_device_id = self.get_credentials()

        self.api_key_description_label = QLabel(self.dictionary["api_key"])
        self.api_key_label = QLabel(self.api_key)
        self.api_key_label.setProperty("class", "bordered_field")
        self.api_key_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.api_secret_description_label = QLabel(self.dictionary["api_secret"])
        self.api_secret_label = QLabel(self.api_secret)
        self.api_secret_label.setProperty("class", "bordered_field")
        self.api_secret_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.api_region_description_label = QLabel(self.dictionary["api_region"])
        self.api_region_label = QLabel(self.api_region)
        self.api_region_label.setProperty("class", "bordered_field")
        self.api_region_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.api_device_id_description_label = QLabel(self.dictionary["api_device_id"])
        self.api_device_id_label = QLabel(self.api_device_id)
        self.api_device_id_label.setProperty("class", "bordered_field")
        self.api_device_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.change_credentials_button = QPushButton(self.dictionary["change_credentials_button"])
        self.change_credentials_button.setProperty("class", "device_button")
        self.change_credentials_button.clicked.connect(lambda: self.parent.parent.parent.show_credentials(self.api_key, self.api_secret, self.api_device_id, self.api_region))
        self.change_credentials_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.glayout.addWidget(self.api_key_description_label, 0, 0)
        self.glayout.addWidget(self.api_key_label, 0, 1)

        self.glayout.addWidget(self.api_secret_description_label, 1, 0)
        self.glayout.addWidget(self.api_secret_label, 1, 1)

        self.glayout.addWidget(self.api_region_description_label, 2, 0)
        self.glayout.addWidget(self.api_region_label, 2, 1)

        self.glayout.addWidget(self.api_device_id_description_label, 3, 0)
        self.glayout.addWidget(self.api_device_id_label, 3, 1)

        self.vlayout.addLayout(self.glayout)

        spacer_item = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.vlayout.addWidget(self.change_credentials_button, Qt.AlignmentFlag.AlignBottom)

    def get_credentials(self):
        if os.path.exists("tinytuya.json"):
            with open("tinytuya.json", "r", encoding="utf-8") as f:
                credentials = json.load(f)
                return credentials["apiKey"], credentials["apiSecret"], credentials["apiRegion"], credentials["apiDeviceID"]
        else:
            return "", "", "", ""
