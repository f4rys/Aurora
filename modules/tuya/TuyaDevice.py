import tinytuya

class TuyaDevice():
    def __init__(self, dev_id, local_key, ip, version, name, icon_link, brightness_range, temperature_range, is_rgb, hsv_range, has_countdown):
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
        self.device.set_timer(sec, 26)