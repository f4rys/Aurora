from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QSpacerItem, QSizePolicy


class CredentialsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(15, 0, 15, 0)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("API key")
        self.api_key_input.setProperty("class", "credentials_input")
        self.vlayout.addWidget(self.api_key_input)

        self.api_secret_input = QLineEdit()
        self.api_secret_input.setPlaceholderText("API secret")
        self.api_secret_input.setProperty("class", "credentials_input")
        self.vlayout.addWidget(self.api_secret_input)

        self.api_device_id_input = QLineEdit()
        self.api_device_id_input.setPlaceholderText("Device ID")
        self.api_device_id_input.setProperty("class", "credentials_input")
        self.vlayout.addWidget(self.api_device_id_input)

        self.api_region_input = QComboBox()
        self.api_region_input.setProperty("class", "credentials_input")
        self.api_region_input.addItems([
            "cn\tChina Data Center", 
            "us\tUS - Western America Data Center", 
            "us-e\tUS - Eastern America Data Center", 
            "eu\tCentral Europe Data Center",
            "eu-w\tWestern Europe Data Center",
            "in\tIndia Data Center"])
        self.vlayout.addWidget(self.api_region_input)

        self.credentials_button = QPushButton("Set credentials")
        self.credentials_button.setProperty("class", "credentials_button")
        self.vlayout.addWidget(self.credentials_button)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)
