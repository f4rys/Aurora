import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from modules.gui import MainWindow

class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setQuitOnLastWindowClosed(False)

        self.window = MainWindow(self)

        if os.path.exists("styles.qss"):
            with open('styles.qss', 'r', encoding="utf-8") as f:
                style = f.read()
                self.setStyleSheet(style)

        tray = QSystemTrayIcon()
        tray.setIcon(QIcon(":/icon/icon.png"))
        tray.setVisible(True)
        tray.activated.connect(self.window.show_window)

        self.exec()

    def restart_window(self):
        self.window.destroy()
        self.window = MainWindow(self)
        self.window.show_window()
