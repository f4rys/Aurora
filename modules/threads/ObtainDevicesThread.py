import json

from PyQt6.QtCore import QThread, pyqtSignal
import tinytuya

class ObtainDevicesThread(QThread):
    finished = pyqtSignal(dict, list)

    def run(self):
        try:
            network_devices = tinytuya.deviceScan()

            devices_file = open('devices.json', encoding="utf-8")
            devices_data = json.load(devices_file)
            devices_file.close()

            self.finished.emit(network_devices, devices_data)
        except Exception as e:
            self.finished.emit({})
