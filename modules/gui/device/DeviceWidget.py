from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from modules.gui.device import BulbNameLabel, BulbSwitchButton
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab, TimerTab
from modules.dictionaries.loader import load_dictionary


class DeviceWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictionary = load_dictionary()
        self.vlayout = QVBoxLayout(self)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def switch(self, device):
        if device.is_on():
            device.turn_off()
            self.bulb_button.set_icon(False)
        else:
            device.turn_on()
            self.bulb_button.set_icon(True)

    def init_ui(self, device):
        self.clear_layout(self.vlayout)

        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.bulb_button = BulbSwitchButton()
        self.bulb_button.set_icon(device.is_on())
        self.bulb_button.clicked.connect(lambda: self.switch(device))
        self.vlayout.addWidget(self.bulb_button)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.setTabBarAutoHide(True)

        self.white_tab = WhiteModeTab()
        self.tab_widget.addTab(self.white_tab, self.dictionary["white"])

        self.colour_tab = ColourModeTab()
        self.tab_widget.addTab(self.colour_tab, self.dictionary["colour"])

        self.timer_tab = TimerTab()
        self.tab_widget.addTab(self.timer_tab, self.dictionary["timer"])

        self.vlayout.addWidget(self.tab_widget)
        self.tab_widget.setCurrentIndex(0)

        #White mode sliders
        self.white_tab.brightness_slider.setRange(device.brightness_range[0], device.brightness_range[1])
        self.white_tab.brightness_slider.valueChanged.connect(lambda: self.set_brightness((device)))

        self.white_tab.temperature_slider.setRange(device.temperature_range[0], device.temperature_range[1])
        self.white_tab.temperature_slider.valueChanged.connect(lambda: self.set_temperature(device))

        self.set_brightness_slider(device)
        self.set_temperature_slider(device)

    def set_brightness(self, device):
        if(self.tab_widget.currentIndex() == 0):
            value = self.white_tab.brightness_slider.value()
        else:
            value = self.colour_tab.brightness_slider.value()
        device.device.set_brightness(value)

    def set_brightness_slider(self, device):
        value = device.get_brightness()
        self.white_tab.brightness_slider.setValue(value)
        self.colour_tab.brightness_slider.setValue(value)

    def set_temperature(self, device):
        value = self.white_tab.temperature_slider.value()
        device.device.set_colourtemp(value)

    def set_temperature_slider(self, device):
        value = device.get_temperature()
        self.white_tab.temperature_slider.setValue(value)
'''
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
'''
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