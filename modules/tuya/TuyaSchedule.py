import json

from modules.tuya import TuyaCloud

class TuyaSchedule():
    def __init__(self, schedule_id, alias_name, time, timezone_id, loops, devices, code, value):
        self.id = schedule_id
        self.alias_name = alias_name
        self.time = time
        self.timezone_id = timezone_id
        self.loops = loops
        self.devices = devices
        self.code = code
        self.value = value

    def save_to_json(self):

        schedules = {}
        try:
            with open("modules/resources/json/schedules.json", "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except FileNotFoundError:
            pass

        schedules[self.id] = {
            "alias_name": self.alias_name,
            "time": self.time,
            "timezone_id": self.timezone_id,
            "loops": self.loops,
            "devices": self.devices,
            "active": True,
            "functions": [{   
                "code": self.code, 
                "value": self.value
                }
            ]
        }

        with open("modules/resources/json/schedules.json", "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=4)

    def save_to_cloud(self):
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

        for device in self.devices:
            if tuya_cloud.cloud is not None:
                response = tuya_cloud.cloud.cloudrequest(url="/v2.0/cloud/timer/device/bff625311501591637uftv", action="GET")
                print(response)

    def remove_from_cloud(self):
        pass

    def modify_on_cloud(self):
        pass

    def disable_on_cloud(self):
        pass
