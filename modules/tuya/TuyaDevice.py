import json

import tinytuya

class TuyaDevice(tinytuya.BulbDevice):
    def __init__(self, dev_id):
        with open('devices.json', encoding='utf-8') as f:
            data = json.load(f)
        key_nodes = [node for node in data if node.get('key') == dev_id]
        local_key = key_nodes[0]['key'] if key_nodes else None

        super().__init__(dev_id, local_key, version=3.3)

    def is_on(self):
        if self.state()['is_on']:
            return True
        else:
            return False
        
    def switch(self):
        if self.state()['is_on']:
            self.turn_off()
        else:
            self.turn_on()
        
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

