from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout

class ColourModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout()

        self.colour_slider = QSlider(parent=self)
        self.colour_slider.setProperty("class", "colour_slider")
        self.colour_slider.setOrientation(Qt.Orientation.Horizontal)

        self.brightness_slider = QSlider(parent=self)
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)

        self.contrast_slider = QSlider(parent=self)
        self.contrast_slider.setProperty("class", "contrast_slider")
        self.contrast_slider.setOrientation(Qt.Orientation.Horizontal)

        self.vlayout.addWidget(self.colour_slider)
        self.vlayout.addWidget(self.brightness_slider)
        self.vlayout.addWidget(self.contrast_slider)
        self.setLayout(self.vlayout)