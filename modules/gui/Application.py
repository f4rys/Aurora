from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from modules.gui import MainWindow

class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setQuitOnLastWindowClosed(False)

        self.window = MainWindow()

        with open('styles.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        icon = QIcon(":/icon/icon.png")
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        tray.activated.connect(lambda: self.window.show_window())

        self.exec()