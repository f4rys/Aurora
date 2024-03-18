from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout


class WhiteModeTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vlayout = QVBoxLayout(self)

        self.brightness_slider = QSlider()
        self.brightness_slider.setProperty("class", "brightness_slider")
        self.brightness_slider.setOrientation(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(10, 1000)
        self.brightness_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.warmth_slider = QSlider()
        self.warmth_slider.setProperty("class", "warmth_slider")
        self.warmth_slider.setOrientation(Qt.Orientation.Horizontal)
        self.warmth_slider.setRange(10, 1000)
        self.warmth_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.vlayout.addWidget(self.brightness_slider)
        self.vlayout.addWidget(self.warmth_slider)
