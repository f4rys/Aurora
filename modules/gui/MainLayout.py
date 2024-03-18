from PyQt6.QtWidgets import QVBoxLayout, QFrame

from modules.gui import StackedWidget


class MainLayout(QVBoxLayout):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        
        self.setContentsMargins(0, 0, 0, 0)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setProperty("class", "hline")
        self.addWidget(self.line)

        self.stacked_widget = StackedWidget(self)
        self.addWidget(self.stacked_widget)

