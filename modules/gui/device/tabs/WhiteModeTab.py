from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout

from modules.dictionaries.loader import load_dictionary

class WhiteModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.vlayout = QVBoxLayout(self)

        self.brightness_slider = QSlider()
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(10, 1000)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightness_slider.setToolTip(self.dictionary["brightness_tooltip"])

        self.warmth_slider = QSlider()
        self.warmth_slider.setProperty("class", "warmth_slider")
        self.warmth_slider.setOrientation(Qt.Orientation.Horizontal)
        self.warmth_slider.setRange(10, 1000)
        self.warmth_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.warmth_slider.setToolTip(self.dictionary["temperature_tooltip"])

        self.vlayout.addWidget(self.brightness_slider)
        self.vlayout.addWidget(self.warmth_slider)
