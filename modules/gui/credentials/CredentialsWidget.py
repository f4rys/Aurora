from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QSpacerItem, QSizePolicy
from pyqttoast import Toast, ToastPreset

from modules.tuya import register

class CredentialsWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

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
        self.api_region_input.setCurrentIndex(3)
        self.vlayout.addWidget(self.api_region_input)

        self.credentials_button = QPushButton("Set credentials")
        self.credentials_button.setProperty("class", "credentials_button")
        self.vlayout.addWidget(self.credentials_button)
        self.credentials_button.clicked.connect(self.send_credentials)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.vlayout.addItem(spacer_item)

    def send_credentials(self):
        api_key = self.api_key_input.text()
        api_secret = self.api_secret_input.text()
        api_device_id = self.api_device_id_input.text()
        api_region_index = self.api_region_input.currentIndex()
        api_region = 'eu'

        if api_region_index == 0:
            api_region = 'cn'
        elif api_region_index == 1:
            api_region = 'us'
        elif api_region_index == 2:
            api_region = 'us-e'
        elif api_region_index == 3:
            api_region = 'eu'
        elif api_region_index == 4:
            api_region = 'eu-w'
        elif api_region_index == 5:
            api_region = 'in'

        status = register(api_key, api_secret, api_region, api_device_id)

        toast = Toast(self)
        toast.setAlwaysOnMainScreen(True)
        toast.setShowDurationBar(False)
        toast.setBorderRadius(15)
        toast.setResetDurationOnHover(False)
        toast.setMaximumWidth(300)
        toast.setMaximumHeight(100)
        toast.setDuration(5000)
        toast.setBackgroundColor(QColor('#DAD9D3'))

        if status:
            toast.setTitle('Success')
            toast.setText('Your Tuya credentials has been set and list of your devices has been updated.')
            toast.applyPreset(ToastPreset.SUCCESS)
            toast.show()

            self.parent.parent.parent.show_all_devices()

        else:
            toast.setTitle('Failure')
            toast.setText('A problem occured. Check if the data you entered is correct and try again.')
            toast.applyPreset(ToastPreset.ERROR)
            toast.show()

            self.api_key_input.clear()
            self.api_secret_input.clear()
            self.api_device_id_input.clear()
            self.api_region_input.setCurrentIndex(3)
