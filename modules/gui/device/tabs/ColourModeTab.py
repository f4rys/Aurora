from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout

from modules.dictionaries.loader import load_dictionary

class ColourModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)

        self.colour_slider = QSlider()
        self.colour_slider.setProperty("class", "colour_slider")
        self.colour_slider.setOrientation(Qt.Orientation.Horizontal)
        self.colour_slider.setToolTip(self.dictionary["colour_tooltip"])

        self.brightness_slider = QSlider()
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brightness_slider.setToolTip(self.dictionary["brightness_tooltip"])

        self.contrast_slider = QSlider()
        self.contrast_slider.setProperty("class", "contrast_slider")
        self.contrast_slider.setOrientation(Qt.Orientation.Horizontal)
        self.contrast_slider.setToolTip(self.dictionary["contrast_tooltip"])

        self.vlayout.addWidget(self.colour_slider)
        self.vlayout.addWidget(self.brightness_slider)
        self.vlayout.addWidget(self.contrast_slider)