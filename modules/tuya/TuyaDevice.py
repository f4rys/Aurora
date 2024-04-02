import tinytuya

class TuyaDevice():
    def __init__(self, dev_id, local_key, ip, version, name, icon_link):
        self.device = tinytuya.BulbDevice(dev_id=dev_id, address=ip, local_key=local_key, version=version)

        self.id = dev_id
        self.local_key = local_key
        self.version = version
        self.name = name
        self.icon_link = icon_link

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
        
    def change_contrast(self, value):
        pass

    def get_contrast(self):
        return 10

'''

    def set_mode(self, mode):
        if mode == 1:
            self.set_mode('colour')
        elif mode == 0:
            self.set_mode('white')

    def get_brightness(self):
        return device.brightness()

    def change_brightness(self, value):
        device.set_brightness(value)

    def get_warmth(self):
        return device.colourtemp()

    def change_warmth(self, value):
        device.set_colourtemp(value)
'''

