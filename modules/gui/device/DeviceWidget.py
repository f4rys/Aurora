from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QFrame

from modules.gui.device import BulbNameLabel, BulbSwitchButton
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab, TimerTab
from modules.tuya import connect, status, turn_off, turn_on, change_brightness, get_brightness, get_warmth, change_warmth, set_mode, change_contrast, get_contrast
from modules import dictionary


class DeviceWidget(QWidget):
    def __init__(self, device_id=123):
        super().__init__()
        
        self.setGeometry(QRect(30, 0, 231, 260))

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setProperty("class", "hline")
        self.vlayout.addWidget(self.line)

        self.label = BulbNameLabel(parent=self, name="RGB748389")
        self.vlayout.addWidget(self.label)

        self.bulb_button = BulbSwitchButton(parent=self)
        self.vlayout.addWidget(self.bulb_button)
        
        self.tab_widget = QTabWidget(parent=self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.setTabBarAutoHide(True)

        self.white_tab = WhiteModeTab()
        self.tab_widget.addTab(self.white_tab, dictionary["white"])

        self.colour_tab = ColourModeTab()
        self.tab_widget.addTab(self.colour_tab, dictionary["colour"])

        self.timer_tab = TimerTab()
        self.tab_widget.addTab(self.timer_tab, dictionary["timer"])

        self.vlayout.addWidget(self.tab_widget)
        self.tab_widget.setCurrentIndex(0)

'''
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

        # WIDGETS

        self.vlayout = QVBoxLayout()
        #self.vlayout.addStretch()
        #self.vlayout.addSpacing(0)
        #self.vlayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vlayout.setContentsMargins(50,10,10,50)
        self.vlayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.name = BulbNameLabel(parent=self, name=self.device_name)
        self.vlayout.addWidget(self.name)

        #self.device = connect(device_id)

        self.bulb = BulbSwitchButton(parent=self)
        self.vlayout.addWidget(self.bulb)
        #self.bulb.clicked.connect(self.switch_bulb)
        #self.set_bulb()

        self.tabs = QTabWidget(parent=self)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.vlayout.addWidget(self.tabs)
        #self.tabs.setGeometry(QRect(0, 160, 200, 100))

        #White mode tab
        self.white_mode = WhiteModeTab(self.tabs)
        self.tabs.addTab(self.white_mode,'White')

        #Colour mode tab
        
        self.colour_mode = ColourModeTab(self.tabs)
        if(self.colour != False):
            self.tabs.addTab(self.colour_mode,'Colour')

        self.timer_tab = TimerTab(self.tabs)
        self.tabs.addTab(self.timer_tab,'Timer')

        self.setLayout(self.vlayout)

        #White mode sliders
        self.white_mode.brightness_slider.setRange(self.brightness_range[0], self.brightness_range[1])
        #self.white_mode.brightness_slider.valueChanged.connect(self.set_brightness)

        self.white_mode.warmth_slider.setRange(self.warmth_range[0], self.warmth_range[1])
        #self.white_mode.warmth_slider.valueChanged.connect(self.set_warmth)

        ##Colour mode sliders

        self.colour_mode.brightness_slider.setRange(self.brightness_range[0], self.brightness_range[1])
        #self.colour_mode.brightness_slider.valueChanged.connect(self.set_brightness)

        self.colour_mode.contrast_slider.setRange(self.warmth_range[0], self.warmth_range[1])
        #self.colour_mode.contrast_slider.valueChanged.connect(self.set_contrast)
        #self.vlayout.addStretch()

        ###
        #self.set_brightness_slider()
        #self.set_warmth_slider()

        #self.tabs.currentChanged.connect(self.set_bulb_mode)

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
        '''