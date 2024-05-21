import json
import os
from collections import defaultdict

from modules.tuya.TuyaCloud import TuyaCloud
from modules.tuya import TuyaSchedule

class TuyaSchedulesManager():
    def __init__(self):
        self.raw_schedules = []
        self.schedules = []
        self.tuya_cloud = TuyaCloud()
        self.empty_schedule = TuyaSchedule("", False, "00:00", "", "0000000", {}, [])

        if os.path.exists('devices.json'):
            try:
                with open('devices.json', 'r', encoding="utf-8") as f:
                    devices_data = json.load(f)

                for device in devices_data:
                    device_id = device.get("id")
                    if self.tuya_cloud.cloud is not None:
                        response = self.tuya_cloud.cloud.cloudrequest(url=f"/v2.0/cloud/timer/device/{device_id}", action="GET")

                        if response is not None:
                            if response["result"]:
                                for i in range(0, len(response["result"])):
                                    schedule = {
                                        device_id: response["result"][i]
                                    }
                                    self.raw_schedules.append(schedule)

                combined_data = defaultdict(dict)

                for item in self.raw_schedules:
                    key, node_data = next(iter(item.items()))
                    alias_name = node_data["alias_name"]
                    timer_id = node_data["timer_id"]

                    # Merge dictionaries, ensuring matching values for other keys
                    for k, v in node_data.items():
                        combined_data[alias_name][k] = v

                    # Collect timer_ids
                    combined_data[alias_name].setdefault("devices_timers", {})[key] = timer_id

                result = list(combined_data.values())

                for item in result:
                    schedule = TuyaSchedule(item["alias_name"],item["enable"], item["time"],item["timezone_id"],item["loops"],item["devices_timers"],item["functions"])
                    self.schedules.append(schedule)
            except Exception:
                pass
