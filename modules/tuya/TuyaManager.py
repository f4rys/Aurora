import json
from configparser import ConfigParser

from tinytuya import deviceScan

from modules.tuya import TuyaDevice

class TuyaManager():
    def __init__(self):
        self.active_devices = {}
        self.inactive_devices = {}
        self.import_devices()

    def import_devices(self):

        self.config = ConfigParser()
        self.config.read('settings.ini')
        max_retry = self.config.get("General", "max_retry")

        network_devices = deviceScan(maxretry=float(max_retry))

        devices_file = open('devices.json', encoding="utf-8")
        devices_data = json.load(devices_file)
        devices_file.close()

        # Active devices
        for device in devices_data:
            device_id = device.get("id")

            for device_info in network_devices.values():
                if device_info.get('id') == device_id:

                    local_key = device_info.get('key')
                    version = device_info.get('version')
                    name = device_info.get('name')
                    ip = device_info.get('ip')
                    icon_link = device.get('icon')

                    brightness_range = [ device["mapping"]["22"]["values"]["min"], device["mapping"]["22"]["values"]["max"] ]
                    temperature_range = [ device["mapping"]["23"]["values"]["min"], device["mapping"]["23"]["values"]["max"] ]

                    if "24" in device["mapping"].keys():
                        is_rgb = True

                        h_range = [ device["mapping"]["24"]["values"]["h"]["min"], device["mapping"]["24"]["values"]["h"]["max"] ]
                        s_range = [ device["mapping"]["24"]["values"]["s"]["min"], device["mapping"]["24"]["values"]["s"]["max"] ]
                        v_range = [ device["mapping"]["24"]["values"]["v"]["min"], device["mapping"]["24"]["values"]["v"]["max"] ]

                        hsv_range = {
                            "h": h_range,
                            "s": s_range,
                            "v": v_range
                        }
                    else:
                        is_rgb = False
                        hsv_range = None

                    if "26" in device["mapping"].keys():
                        has_countdown = True
                        countdown_range = [ device["mapping"]["26"]["values"]["min"], device["mapping"]["26"]["values"]["max"] ]
                    else:
                        has_countdown = False
                        countdown_range = None

                    bulb_device = TuyaDevice(device_id, local_key, ip, version, name, icon_link, brightness_range, temperature_range, is_rgb, hsv_range, has_countdown, countdown_range)
                    self.active_devices[device_id] = bulb_device
                    break

        # Inactive devices
        for device in devices_data:
            device_id = device.get("id")

            if device_id not in self.active_devices:
                name = device.get("name")
                icon_link = device.get("icon")
                self.inactive_devices.update({device_id: {"name": name, "icon_link": icon_link} })
