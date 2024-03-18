import json

import tinytuya

def scan_network():
    return tinytuya.deviceScan()

def connect(device_id):
    try:
        with open('devices.json') as f:
            data = json.load(f)

        key_nodes = [node for node in data if node.get('key') == device_id]

        local_key = key_nodes[0]['key'] if key_nodes else None

        device = tinytuya.BulbDevice(dev_id=device_id, local_key=local_key, version=3.3)
        return device

    except:
        print("Cannot initialize tuya")
        return False
    
def turn_on(device):
    device.turn_on()

def turn_off(device):
    device.turn_off()

def status(device):
    if(device.state()['is_on']):
        return True
    else:
        return False
    
def get_brightness(device):
    return device.brightness()

def change_brightness(device, value):
    device.set_brightness(value)

def get_warmth(device):
    return device.colourtemp()

def change_warmth(device, value):
    device.set_colourtemp(value)

def set_mode(device, mode):
    if(mode == 1):
        device.set_mode('colour')
    elif(mode == 0):
        device.set_mode('white')


def change_contrast(device, value):
    pass

def get_contrast(device):
    return 10