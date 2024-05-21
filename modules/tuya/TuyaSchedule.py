import requests

from modules.tuya.TuyaCloud import TuyaCloud

class TuyaSchedule():
    def __init__(self, alias_name, enable, time, timezone_id, devices_timers, functions, loops=None, category=None, date=None):
        self.alias_name = alias_name
        self.enable = enable
        self.time = time
        self.timezone_id = timezone_id
        self.devices_timers = devices_timers
        self.functions = functions
        self.loops = loops
        self.category = category
        self.date = date

    def save_to_cloud(self):
        response_states = []
        tuya_cloud = TuyaCloud()

        if self.loops is not None:
            schedule = {
                "alias_name": self.alias_name,
                "time": self.time,
                "timezone_id": self.timezone_id,
                "loops": self.loops,
                "functions": self.functions
            }
        elif self.category is not None and self.date is not None:
            schedule = {
                "alias_name": self.alias_name,
                "time": self.time,
                "category": self.category,
                "date": self.date,
                "timezone_id": self.timezone_id,
                "functions": self.functions
            }

        for device in self.devices_timers.keys():
            if tuya_cloud.cloud is not None:
                response = tuya_cloud.cloud.cloudrequest(url=f"/v2.0/cloud/timer/device/{device}", action="POST", post=schedule)
                if response and response["success"]:
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
                response = tuya_cloud.request_on_cloud(url=f"/v2.0/cloud/timer/device/{device}/batch", action="DELETE", query={"timer_ids": timer}, token=token)
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
                    "functions": self.functions
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
