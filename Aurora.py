from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from modules.gui import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    aurora = MainWindow()

    with open('styles.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    icon = QIcon(":/icon/icon.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.activated.connect(lambda: aurora.show_window())

    app.exec()
