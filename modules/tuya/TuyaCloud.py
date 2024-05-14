import os
import json

from tinytuya import Cloud

class TuyaCloud():
    def __init__(self):
        if os.path.exists("tinytuya.json"):
            with open("tinytuya.json", "r", encoding="utf-8") as f:
                credentials = json.load(f)
        else:
            credentials = {'apiKey': '', 'apiSecret': '', 'apiRegion': '', 'apiDeviceID': ''}

        self.api_key = credentials["apiKey"]
        self.api_secret = credentials["apiSecret"]
        self.api_region = credentials["apiRegion"]
        self.api_device_id = credentials["apiDeviceID"]

        try:
            self.cloud = Cloud(apiRegion=self.api_region, apiKey=self.api_key, apiDeviceID=self.api_device_id, apiSecret=self.api_secret)
        except:
            self.cloud = None
