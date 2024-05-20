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
        except Exception:
            self.cloud = None

    def request_on_cloud(self, action, url, token, body=None, query=None):
        # Build URL and Header
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

        if url[0] == '/':
            url = f"https://{endpoint}{url}"
        else:
            url = f"https://{endpoint}/{url}"

        headers = {}
        sign_url = url
        content_type = None
        if body is not None:
            body = json.dumps(body)
        if action == 'DELETE':
            content_type = 'application/json'
        if content_type:
            headers['Content-type'] = content_type
        if query:
            # note: signature must be calculated before URL-encoding!
            if type(query) == str:
                # if it's a string then assume no url-encoding is needed
                if query[0] == '?':
                    url += query
                else:
                    url += '?' + query
                sign_url = url
            else:
                # dicts are unsorted, however Tuya requires the keys to be in alphabetical order for signing
                #  as per https://developer.tuya.com/en/docs/iot/singnature?id=Ka43a5mtx1gsc
                if type(query) == dict:
                    sorted_query = []
                    for k in sorted(query.keys()):
                        sorted_query.append( (k, query[k]) )
                    query = sorted_query
                    # calculate signature without url-encoding
                    sign_url += '?' + '&'.join( [str(x[0]) + '=' + str(x[1]) for x in query] )
                    req = requests.Request(action, url, params=query).prepare()
                    url = req.url
                else:
                    req = requests.Request(action, url, params=query).prepare()
                    sign_url = url = req.url
        now = int(time.time()*1000)
        headers = dict(list(headers.items()) + [('Signature-Headers', ":".join(headers.keys()))]) if headers else {}
        if token is None:
            payload = self.api_key + str(now)
            headers['secret'] = self.api_secret
        else:
            payload = self.api_key + token + str(now)

        new_sign_algorithm = True
        # If running the post 6-30-2021 signing algorithm update the payload to include it's data
        if new_sign_algorithm:
            payload += ('%s\n' % action +                                                # HTTPMethod
                hashlib.sha256(bytes((body or "").encode('utf-8'))).hexdigest() + '\n' + # Content-SHA256
                ''.join(['%s:%s\n'%(key, headers[key])                                   # Headers
                            for key in headers.get("Signature-Headers", "").split(":")
                            if key in headers]) + '\n' +
                '/' + sign_url.split('//', 1)[-1].split('/', 1)[-1]) # type: ignore
        # Sign Payload
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msg=payload.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()

        # Create Header Data
        headers['client_id'] = self.api_key
        headers['sign'] = signature
        headers['t'] = str(now)
        headers['sign_method'] = 'HMAC-SHA256'
        headers['mode'] = 'cors'

        if token is not None:
            headers['access_token'] = token

        if action == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5) # type: ignore
        elif action == "PUT":
            response = requests.put(url, headers=headers, data=body, timeout=5) # type: ignore
        else:
            response = ""
        return response
