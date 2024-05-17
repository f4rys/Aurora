import requests

from modules.tuya.TuyaCloud import TuyaCloud

class TuyaSchedule():
    def __init__(self, alias_name, enable, time, timezone_id, loops, devices_timers, code, value):
        self.alias_name = alias_name
        self.enable = enable
        self.time = time
        self.timezone_id = timezone_id
        self.loops = loops
        self.devices_timers = devices_timers
        self.code = code
        self.value = value

    def save_to_cloud(self):
        response_states = []
        tuya_cloud = TuyaCloud()
        schedule = {
            "alias_name": self.alias_name,
            "time": self.time,
            "timezone_id": self.timezone_id,
            "loops": self.loops,
            "functions": [{   
                "code": self.code, 
                "value": self.value
                }
            ]
        }

        for device in self.devices_timers.keys():
            if tuya_cloud.cloud is not None:
                response = tuya_cloud.cloud.cloudrequest(url=f"/v2.0/cloud/timer/device/{device}", action="POST", post=schedule)
                if isinstance(response, requests.Response) and response.json()["success"]:
                    response_states.append(True)
                else:
                    response_states.append(False)

        return response_states

    def remove_from_cloud(self):
        response_states = []
        tuya_cloud = TuyaCloud()
        
        for device, timer in self.devices_timers.items():
            if tuya_cloud.cloud is not None:
                token = tuya_cloud.cloud.token
                response = tuya_cloud.request_on_cloud(url=f"/v2.0/cloud/timer/device/{device}/batch", action="DELETE", body={"timer_ids": timer}, token=token)
                if isinstance(response, requests.Response) and response.json()["success"]:
                    response_states.append(True)
                else:
                    response_states.append(False)

        return response_states

    def modify_on_cloud(self):
        response_states = []
        tuya_cloud = TuyaCloud()

        for device, timer in self.devices_timers.items():
            if tuya_cloud.cloud is not None:

                schedule = {
                    "timer_id": timer,
                    "alias_name": self.alias_name,
                    "time": self.time,
                    "timezone_id": self.timezone_id,
                    "loops": self.loops,
                    "functions": [{   
                        "code": self.code, 
                        "value": self.value
                        }
                    ]
                }

                token = tuya_cloud.cloud.token
                response = tuya_cloud.request_on_cloud(url=f"/v2.0/cloud/timer/device/{device}", action="PUT", body=schedule, token=token)
                if isinstance(response, requests.Response) and response.json()["success"]:
                    response_states.append(True)
                else:
                    response_states.append(False)

        return response_states

    def change_state_on_cloud(self, state):
        response_states = []
        tuya_cloud = TuyaCloud()

        for device, timer in self.devices_timers.items():
            body = {
                "timer_id": timer,
                "enable": state
            }

            if tuya_cloud.cloud is not None:
                token = tuya_cloud.cloud.token
                response = tuya_cloud.request_on_cloud(url=f"/v2.0/cloud/timer/device/{device}/state", action="PUT", token=token, body=body)
                if isinstance(response, requests.Response) and response.json()["success"]:
                    response_states.append(True)
                else:
                    response_states.append(False)

        return response_states
