from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QSlider, QWidget

class ColourModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.colour_slider = QSlider(parent=self)
        self.colour_slider.setProperty("class", "colour_slider")
        self.colour_slider.setGeometry(QRect(25,5,150,20))
        self.colour_slider.setOrientation(Qt.Orientation.Horizontal)

        self.brightness_slider = QSlider(parent=self)
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setGeometry(QRect(25,30,150,20))
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)

        self.contrast_slider = QSlider(parent=self)
        self.contrast_slider.setProperty("class", "contrast_slider")
        self.contrast_slider.setGeometry(QRect(25,55,150,20))
        self.contrast_slider.setOrientation(Qt.Orientation.Horizontal)