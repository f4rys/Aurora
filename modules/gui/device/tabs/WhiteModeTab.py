from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QSlider, QWidget

class WhiteModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.brightness_slider = QSlider(parent=self)
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setGeometry(QRect(25,10,150,20))
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(10, 1000)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.warmth_slider = QSlider(parent=self)
        self.warmth_slider.setProperty("class", "warmth_slider")
        self.warmth_slider.setGeometry(QRect(25,40,150,20))
        self.warmth_slider.setOrientation(Qt.Orientation.Horizontal)
        self.warmth_slider.setRange(10, 1000)
        self.warmth_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
