from PyQt6.QtGui import QColor
from pyqttoast import Toast, ToastPreset

from modules.dictionaries import load_dictionary

def show_error_toast(parent):
    dictionary = load_dictionary()
    toast = Toast(parent)
    toast.setAlwaysOnMainScreen(True)
    toast.setShowDurationBar(False)
    toast.setBorderRadius(15)
    toast.setResetDurationOnHover(False)
    toast.setMaximumWidth(300)
    toast.setMaximumHeight(100)
    toast.setDuration(5000)
    toast.setBackgroundColor(QColor('#DAD9D3'))
    toast.setTitle(dictionary["error_toast_title"])
    toast.setText(dictionary["error_toast_body"])
    toast.applyPreset(ToastPreset.ERROR)
    toast.show()
