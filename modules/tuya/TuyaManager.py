import json

import tinytuya

from modules.tuya import TuyaDevice

class TuyaManager():
    def __init__(self):
        self.active_devices = {}
        self.inactive_devices = {}
        self.import_devices()

    def import_devices(self):
        network_devices = tinytuya.deviceScan()

        devices_file = open('devices.json', encoding="utf-8")
        devices_data = json.load(devices_file)
        devices_file.close()

        # Active devices
        for device in devices_data:
            device_id = device.get("id")

            for ip_address, device_info in network_devices.items():
                if device_info.get('id') == device_id:
                    
                    local_key = device_info.get('key')
                    version = device_info.get('version')
                    name = device_info.get('name')
                    ip = device_info.get('ip')
                    icon_link = device.get('icon')

                    bulb_device = TuyaDevice(device_id, local_key, ip, version, name, icon_link)
                    self.active_devices[device_id] = bulb_device
                    break

        # Inactive devices
        for device in devices_data:
            device_id = device.get("id")

            if device_id not in self.active_devices:
                id = device.get("id")
                name = device.get("name")
                icon_link = device.get("icon")

                self.inactive_devices.update({id: {"name": name, "icon_link": icon_link} })
                #self.inactive_devices[id]["icon_link"] = icon_link
