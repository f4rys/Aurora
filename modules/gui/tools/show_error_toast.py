from PyQt6.QtGui import QColor
from pyqttoast import Toast, ToastPreset

def show_error_toast(parent):
    toast = Toast(parent)
    toast.setAlwaysOnMainScreen(True)
    toast.setShowDurationBar(False)
    toast.setBorderRadius(15)
    toast.setResetDurationOnHover(False)
    toast.setMaximumWidth(300)
    toast.setMaximumHeight(100)
    toast.setDuration(5000)
    toast.setBackgroundColor(QColor('#DAD9D3'))
    toast.setTitle('Failure')
    toast.setText('A problem occured. Try later.')
    toast.applyPreset(ToastPreset.ERROR)
    toast.show()