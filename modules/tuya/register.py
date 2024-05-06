from __future__ import print_function
import json
from datetime import datetime
import tinytuya

DEVICEFILE = tinytuya.DEVICEFILE
SNAPSHOTFILE = tinytuya.SNAPSHOTFILE
CONFIGFILE = tinytuya.CONFIGFILE
RAWFILE = tinytuya.RAWFILE
DEFAULT_NETWORK = tinytuya.DEFAULT_NETWORK
TCPTIMEOUT = tinytuya.TCPTIMEOUT
TCPPORT = tinytuya.TCPPORT

def register(api_key, api_secret, api_region, api_device_id):

    config = {}
    config['apiKey'] = api_key
    config['apiSecret'] = api_secret
    config['apiRegion'] = api_region
    config['apiDeviceID'] = api_device_id

    json_object = json.dumps(config, indent=4)
    with open(CONFIGFILE, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

    cloud = tinytuya.Cloud( **config )

    if cloud.error:
        return False

    tuyadevices = cloud.getdevices(verbose=False, oldlist={}, include_map=True)

    if isinstance(tuyadevices, list):
        return False

    for dev in tuyadevices:
        if 'gateway_id' in dev:
            if dev['gateway_id']:
                dev['parent'] = dev['gateway_id']
            del dev['gateway_id']

        if 'sub' in dev and dev['sub']:
            if 'parent' in dev and dev['parent']:
                continue

            dev['parent'] = ''

            if 'key' in dev and dev['key']:
                if 'id' not in dev:
                    dev['id'] = ''
                found = False
                for parent in tuyadevices:
                    if 'id' not in parent or parent['id'] == dev['id']:
                        continue
                    if 'key' in parent and parent['key'] and dev['key'] == parent['key'] and ( 'sub' not in parent or not parent['sub']):
                        found = parent
                        break
                if found:
                    dev['parent'] = found['id']

    output = json.dumps(tuyadevices, indent=4)

    with open(DEVICEFILE, "w", encoding="utf-8") as outfile:
        outfile.write(output)

    cloud.getdevices_raw['file'] = { # type: ignore
        'name': RAWFILE,
        'description': 'Full raw list of Tuya devices.',
        'account': cloud.apiKey,
        'date': datetime.now().isoformat(),
        'tinytuya': tinytuya.version
    }
    try:
        with open(RAWFILE, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(cloud.getdevices_raw, indent=4))
    except:
        return False

    return True

def check_credentials():
    try:
        with open(CONFIGFILE, encoding="utf-8") as f:
            config = json.load(f)
            if (config['apiKey'] != '' and config['apiSecret'] != '' and config['apiRegion'] != ''):
                return True
            return False
    except:
        return False
