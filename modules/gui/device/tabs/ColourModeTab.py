from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout

from modules.dictionaries.loader import load_dictionary

class ColourModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)

        self.hue_slider = QSlider()
        self.hue_slider.setProperty("class", "colour_slider")
        self.hue_slider.setOrientation(Qt.Orientation.Horizontal)
        self.hue_slider.setToolTip(self.dictionary["colour_tooltip"])

        self.saturation_slider = QSlider()
        self.saturation_slider.setProperty("class", "contrast_slider")
        self.saturation_slider.setOrientation(Qt.Orientation.Horizontal)
        self.saturation_slider.setToolTip(self.dictionary["contrast_tooltip"])

        self.value_slider = QSlider()
        self.value_slider.setProperty("class", "brightness_slider")
        self.value_slider.setOrientation(Qt.Orientation.Horizontal)
        self.value_slider.setToolTip(self.dictionary["brightness_tooltip"])

        self.vlayout.addWidget(self.hue_slider)
        self.vlayout.addWidget(self.saturation_slider)
        self.vlayout.addWidget(self.value_slider)
        
