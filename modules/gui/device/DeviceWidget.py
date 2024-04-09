from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from modules.gui.device import BulbSwitchButton
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab, CountdownTab
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

    def switch(self):
        if self.device.is_on():
            self.device.turn_off()
            self.change_icon()
        else:
            self.device.turn_on()
            self.change_icon()

    def change_icon(self):
        if self.device.is_on():
            self.bulb_button.set_icon(True)
        else:
            self.bulb_button.set_icon(False)

    def init_ui(self, device):
        self.clear_layout(self.vlayout)

        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.device = device
        self.is_rgb = self.device.is_rgb

        self.bulb_button = BulbSwitchButton()
        self.bulb_button.set_icon(device.is_on())
        self.bulb_button.clicked.connect(self.switch)
        self.vlayout.addWidget(self.bulb_button)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.setTabBarAutoHide(True)

        self.white_tab = WhiteModeTab()
        self.tab_widget.addTab(self.white_tab, self.dictionary["white"])

        if self.is_rgb:
            self.colour_tab = ColourModeTab()
            self.tab_widget.addTab(self.colour_tab, self.dictionary["colour"])

            self.colour_tab.hue_slider.setRange(device.hsv_range["h"][0], device.hsv_range["h"][1])
            self.colour_tab.saturation_slider.setRange(device.hsv_range["s"][0], device.hsv_range["s"][1])
            self.colour_tab.value_slider.setRange(device.hsv_range["v"][0] + 10, device.hsv_range["v"][1])

            self.colour_tab.hue_slider.valueChanged.connect(self.set_hsv)
            self.colour_tab.saturation_slider.valueChanged.connect(self.set_hsv)
            self.colour_tab.value_slider.valueChanged.connect(self.set_hsv)

        self.countdown_tab = CountdownTab(self)
        self.tab_widget.addTab(self.countdown_tab, self.dictionary["countdown"])

        self.vlayout.addWidget(self.tab_widget)

        self.white_tab.brightness_slider.setRange(device.brightness_range[0], device.brightness_range[1])
        self.white_tab.brightness_slider.valueChanged.connect(self.set_brightness)

        self.white_tab.temperature_slider.setRange(device.temperature_range[0], device.temperature_range[1])
        self.white_tab.temperature_slider.valueChanged.connect(self.set_temperature)

        self.set_initial_tab()
        self.tab_widget.currentChanged.connect(self.set_bulb_mode)

    def set_initial_tab(self):
        mode = self.device.get_mode()

        self.get_slider_values(mode)

        if mode == "white":
            self.tab_widget.setCurrentIndex(0)
        elif mode == "colour":
            self.tab_widget.setCurrentIndex(1)

    def get_slider_values(self, index):
        if index == "colour":
            self.set_hsv_sliders()
        elif index == "white":
            self.set_brightness_slider()
            self.set_temperature_slider()

    def set_bulb_mode(self, index):
        self.device.set_mode(index)
        self.get_slider_values(self.device.get_mode())

    def set_brightness(self):
        if self.tab_widget.currentIndex() == 0:
            value = self.white_tab.brightness_slider.value()
        else:
            value = self.colour_tab.value_slider.value()
        self.device.device.set_brightness(value)

    def set_brightness_slider(self):
        value = self.device.get_brightness()
        self.white_tab.brightness_slider.setValue(value)

    def set_temperature(self):
        value = self.white_tab.temperature_slider.value()
        self.device.device.set_colourtemp(value)

    def set_temperature_slider(self):
        value = self.device.get_temperature()
        self.white_tab.temperature_slider.setValue(value)

    def set_hsv(self):
        h = self.colour_tab.hue_slider.value()
        s = self.colour_tab.saturation_slider.value()
        v = self.colour_tab.value_slider.value()

        self.device.set_hsv(h, s, v)

    def set_hsv_sliders(self):
        h, s, v = self.device.get_hsv()

        h = h * self.device.hsv_range["h"][1]
        s = s * self.device.hsv_range["s"][1]
        v = v * self.device.hsv_range["v"][1]

        self.colour_tab.hue_slider.setValue(int(h))
        self.colour_tab.saturation_slider.setValue(int(s))
        self.colour_tab.value_slider.setValue(int(v))
