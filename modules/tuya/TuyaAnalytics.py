import json
import os

import pandas as pd
import matplotlib.pyplot as plt

from modules.tuya.TuyaCloud import TuyaCloud

class TuyaAnalytics():
    def __init__(self):
        self.tuya_cloud = TuyaCloud()

    def get_devices_logs(self):
        if self.tuya_cloud.cloud is not None:
            with open("devices.json", encoding="utf-8") as devices_file:
                devices_data = json.load(devices_file)

            for device in devices_data:
                filename = f'modules/resources/json/logs/{device["id"]}.json'

                try:
                    with open(filename, 'r', encoding="utf-8") as logs_file:
                        existing_logs = json.load(logs_file)
                except FileNotFoundError:
                    existing_logs = []

                new_logs = self.tuya_cloud.cloud.getdevicelog(device["id"], start=-7)['result']['logs']

                existing_event_times = set(log["event_time"] for log in existing_logs)
                filtered_logs = [log for log in new_logs if log["event_time"] not in existing_event_times]

                all_logs = existing_logs + filtered_logs

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                with open(filename, 'w', encoding="utf-8") as logs_file:
                    json.dump(all_logs, logs_file) 

    def create_plot(self, devices):
        df = pd.DataFrame()

        for device in devices:
            with open(f'modules/resources/json/logs/{device}.json', 'r', encoding="utf-8") as file:
                data = json.load(file)
            temp_df = pd.DataFrame(data)

            df = pd.concat([temp_df, df])

        df['event_time'] = pd.to_datetime(df['event_time'], unit='ms')
        df['date_str'] = df['event_time'].dt.strftime('%m.%d')
        day_counts = df['date_str'].value_counts(sort=False)

        today = pd.Timestamp('today')  # Get today's date
        seven_days_ago = today - pd.Timedelta(days=6)
        date_range = pd.date_range(seven_days_ago, today).strftime('%m.%d')

        day_counts = day_counts.reindex(date_range, fill_value=0)

        figure, ax = plt.subplots(figsize=(10, 10))

        ax.bar(day_counts.index, day_counts.values, color='#00ceff') # type: ignore

        for i, value in enumerate(day_counts.values):
            ax.text(i, value + 2, str(value), ha='center', va='bottom', fontsize=7)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])

        ax.tick_params(bottom=False, left=False, labelsize=7, rotation=45)
        ax.set_xticks(day_counts.index)
        plt.subplots_adjust(bottom=0.2)

        return figure
