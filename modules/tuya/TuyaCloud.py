import os
import json
import hmac
import time
import hashlib

import requests
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

    def request_on_cloud(self, action, url, body, token):
        endpoint = "openapi.tuyacn.com"          # China Data Center
        if self.api_region == "us":
            endpoint = "openapi.tuyaus.com"      # Western America Data Center
        if self.api_region == "us-e":
            endpoint = "openapi-ueaz.tuyaus.com" # Eastern America Data Center
        if self.api_region == "eu":
            endpoint = "openapi.tuyaeu.com"      # Central Europe Data Center
        if self.api_region == "eu-w":
            endpoint = "openapi-weaz.tuyaeu.com" # Western Europe Data Center
        if self.api_region == "in":
            endpoint = "openapi.tuyain.com"      # India Datacenter

        headers = {}
        body = json.dumps(body)

        if url[0] == '/':
            url = "https://%s%s" % (endpoint, url)
        else:
            url = "https://%s/%s" % (endpoint, url)
        
        now = int(time.time()*1000)
        headers = dict(list(headers.items()) + [('Signature-Headers', ":".join(headers.keys()))]) if headers else {}

        if token is None:
            payload = self.api_key + str(now)
            headers['secret'] = self.api_secret
        else:
            payload = self.api_key + token + str(now)

        payload += ('%s\n' % action +                                                # HTTPMethod
            hashlib.sha256(bytes((body or "").encode('utf-8'))).hexdigest() + '\n' + # Content-SHA256 # type: ignore
            ''.join(['%s:%s\n'%(key, headers[key])                                   # Headers
                        for key in headers.get("Signature-Headers", "").split(":")
                        if key in headers]) + '\n' +
            '/' + url.split('//', 1)[-1].split('/', 1)[-1])
        # Sign Payload
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msg=payload.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()

        headers['client_id'] = self.api_key
        headers['sign'] = signature
        headers['t'] = str(now)
        headers['sign_method'] = 'HMAC-SHA256'
        headers['mode'] = 'cors'
        headers['access_token'] = token

        if action == "DELETE":
            response = requests.delete(url, headers=headers, data=body)
        elif action == "PUT":
            response = requests.put(url, headers=headers, data=body)
        else:
            response = ""
        return response
