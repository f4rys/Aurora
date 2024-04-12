import os
import json
import time

import tinytuya

class TuyaDevice():
    def __init__(self, dev_id, local_key, ip, version, name, icon_link, brightness_range, temperature_range, is_rgb, hsv_range, has_countdown, countdown_range):
        self.device = tinytuya.BulbDevice(dev_id=dev_id, address=ip, local_key=local_key, version=version)

        self.id = dev_id
        self.local_key = local_key
        self.version = version
        self.name = name
        self.icon_link = icon_link
        self.brightness_range = brightness_range
        self.temperature_range = temperature_range
        self.is_rgb = is_rgb
        self.hsv_range = hsv_range
        self.has_countdown = has_countdown
        self.countdown_range = countdown_range

    def read_current_countdown(self):
        try:
            if os.path.exists("modules/resources/countdowns/countdowns.json"):
                with open("modules/resources/countdowns/countdowns.json", "r", encoding="utf-8") as f:
                    countdowns = json.load(f)
            else:
                return 0

            if self.device.id in countdowns.keys():
                if countdowns[self.device.id] < time.time():
                    self.delete_countdown()
                    return 0
                else:
                    return countdowns[self.device.id]
            else:
                return 0
        except:
            return 0

    def turn_on(self):
        self.device.turn_on()

    def turn_off(self):
        self.device.turn_off()

    def is_on(self):
        try:
            if self.device.state()['is_on']:
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_brightness(self):
        return self.device.brightness()

    def get_temperature(self):
        return self.device.colourtemp()

    def set_mode(self, mode):
        if mode == 1:
            self.device.set_mode('colour')
        elif mode == 0:
            self.device.set_mode('white')

    def get_mode(self):
        return self.device.state()["mode"]

    def set_hsv(self, h, s, v):
        h = h / self.hsv_range["h"][1]
        s = s / self.hsv_range["s"][1]
        v = v / self.hsv_range["v"][1]

        self.device.set_hsv(h, s, v)

    def get_hsv(self):
        return self.device.colour_hsv()

    def set_countdown(self, sec):
        with open("modules/resources/countdowns/countdowns.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data[self.id] = time.time() + sec

            f.seek(0)
            json.dump(data, f)

        self.device.set_timer(sec, 26)

    def delete_countdown(self):
        with open("modules/resources/countdowns/countdowns.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        if self.id in data:
            data.pop(self.id)

        with open("modules/resources/countdowns/countdowns.json", 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def cancel_countdown(self):
        self.device.set_timer(0, 26)
        self.delete_countdown()
