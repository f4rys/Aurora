from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QTabWidget

from modules.gui.device.BulbNameLabel import BulbNameLabel
from modules.gui.device.BulbSwitchButton import BulbSwitchButton
from modules.gui.device.tabs.ColourModeTab import ColourModeTab
from modules.gui.device.tabs.WhiteModeTab import WhiteModeTab
from modules.gui.device.tabs.TimerTab import TimerTab

from modules.tuya.tuya import connect, status, turn_off, turn_on, change_brightness, get_brightness, get_warmth, change_warmth, set_mode, change_contrast, get_contrast

import json

class DeviceWidget(QWidget):
    def __init__(self, device_id):
        super().__init__()

        with open('devices.json', 'r') as file:
            data = json.load(file)

        matching_node = next((node for node in data if node.get("id") == device_id), None)

        self.brightness_range = [matching_node["mapping"]["22"]["values"]["min"] if matching_node else 0, matching_node["mapping"]["22"]["values"]["max"] if matching_node else 10000]
        self.warmth_range = [matching_node["mapping"]["23"]["values"]["min"] if matching_node else 0, matching_node["mapping"]["23"]["values"]["max"] if matching_node else 10000]
        if(matching_node):
            self.colour = "24" in matching_node["mapping"]
        else:
            self.colour = False

        self.device_name = matching_node["name"] if matching_node else "ERROR"

        self.name = BulbNameLabel(parent=self, name=self.device_name)

        self.device = connect(device_id)

        self.bulb = BulbSwitchButton(parent=self)
        self.bulb.clicked.connect(self.switch_bulb)
        self.set_bulb()

        self.tabs = QTabWidget(parent=self)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.tabs.setGeometry(QRect(0, 160, 200, 100))

        #White mode tab
        self.white_mode = WhiteModeTab(self.tabs)
        self.tabs.addTab(self.white_mode,'White')

        #Colour mode tab
        
        self.colour_mode = ColourModeTab(self.tabs)
        if(self.colour != False):
            self.tabs.addTab(self.colour_mode,'Colour')

        self.timer_tab = TimerTab(self.tabs)
        self.tabs.addTab(self.timer_tab,'Timer')

        #White mode sliders
        self.white_mode.brightness_slider.setRange(self.brightness_range[0], self.brightness_range[1])
        self.white_mode.brightness_slider.valueChanged.connect(self.set_brightness)

        self.white_mode.warmth_slider.setRange(self.warmth_range[0], self.warmth_range[1])
        self.white_mode.warmth_slider.valueChanged.connect(self.set_warmth)

        ##Colour mode sliders

        self.colour_mode.brightness_slider.setRange(self.brightness_range[0], self.brightness_range[1])
        self.colour_mode.brightness_slider.valueChanged.connect(self.set_brightness)

        self.colour_mode.contrast_slider.setRange(self.warmth_range[0], self.warmth_range[1])
        self.colour_mode.contrast_slider.valueChanged.connect(self.set_contrast)

        ###
        self.set_brightness_slider()
        self.set_warmth_slider()

        self.tabs.currentChanged.connect(self.set_bulb_mode)

    def switch_bulb(self):
        if(status(self.device)):
            turn_off(self.device)
        else:
            turn_on(self.device)
        self.set_bulb()

    def set_bulb(self):
        if(status(self.device)):
            self.bulb.setStyleSheet("image : url(:/device/bulb_on.png);")
        else:
            self.bulb.setStyleSheet("image : url(:/device/bulb_off.png);")

    def set_brightness(self):
        if(self.tabs.currentIndex() == 0):
            value = self.white_mode.brightness_slider.value()
        else:
            value = self.colour_mode.brightness_slider.value()
        change_brightness(self.device, value)

    def set_brightness_slider(self):
        value = get_brightness(self.device)
        self.white_mode.brightness_slider.setValue(value)
        self.colour_mode.brightness_slider.setValue(value)

    def set_warmth(self):
        value = self.white_mode.warmth_slider.value()
        change_warmth(self.device, value)

    def set_contrast(self):
        value = self.colour_mode.contrast_slider.value()
        change_contrast(self.device, value)

    def set_contrast_slider(self):
        value = get_contrast(self.device)
        self.colour_mode.contrast_slider.setValue(value)

    def set_warmth_slider(self):
        value = get_warmth(self.device)
        self.white_mode.warmth_slider.setValue(value)

    def set_bulb_mode(self, index):
        set_mode(self.device, index)