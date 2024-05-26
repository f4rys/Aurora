import os
import json
import random
import string
import colorsys
from datetime import datetime, timedelta, date

from tzlocal import get_localzone

import pandas as pd
from prophet import Prophet

from modules.tuya import TuyaSchedule, TuyaSchedulesManager

class TuyaSmartMode():
    def __init__(self):
        today = date.today()
        self.last_prediction = today
        file_path = r"modules\resources\json\predictions.json"

        self.delete_used_schedules()

        if not os.path.exists(file_path):
            data = {"last_prediction": today.strftime('%Y-%m-%d')}
            with open(file_path, 'w', encoding="utf-8") as f:
                json.dump(data, f)

            self.smart_mode()
        else:
            with open(file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)

            last_prediction_str = data["last_prediction"]
            last_prediction_date = datetime.strptime(last_prediction_str, '%Y-%m-%d').date()

            if last_prediction_date < today:
                data["last_prediction"] = today.strftime('%Y-%m-%d')
                with open(file_path, 'w', encoding="utf-8") as f:
                    json.dump(data, f)
                self.smart_mode()

    def delete_used_schedules(self):
        manager = TuyaSchedulesManager("smart_mode")

        today = date.today()
        now = datetime.now().time()

        try:
            for schedule in manager.schedules:
                target_date = datetime.strptime(schedule.date, "%Y%m%d").date()
                target_time = datetime.strptime(schedule.time, "%H:%M").time()
                if target_date < today:
                    schedule.remove_from_cloud()
                if target_date == today:
                    if target_time <= now:
                        schedule.remove_from_cloud()
        except Exception:
            pass

    def save_as_schedules(self, predictions):
        for prediction in predictions:
            target_time = datetime.strptime(prediction["time"], "%H:%M").time()
            now = datetime.now().time()
            if target_time > now:
                schedule = TuyaSchedule(alias_name=prediction["alias_name"],
                                        enable=prediction["enable"],
                                        time=prediction["time"],
                                        timezone_id=prediction["timezone_id"],
                                        category=prediction["category"],
                                        devices_timers=prediction["devices_timers"],
                                        date=prediction["date"],
                                        functions=prediction["functions"])
                schedule.save_to_cloud()

    def smart_mode(self):
        df = self.create_dataframe()
        predicted_actions = self.predict(df)
        formatted_predictions = self.format_predictions(predicted_actions)
        self.save_as_schedules(formatted_predictions)

    def create_dataframe(self):
        directory = 'modules/resources/json/logs'
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

        dfs = []
        for file in json_files:
            file_path = os.path.join(directory, file)
            df = pd.read_json(file_path)
            df['device_id'] = os.path.basename(file_path).split('.')[0]
            dfs.append(df)

        final_df = pd.concat(dfs, ignore_index=True)

        final_df = final_df[['device_id', 'code', 'event_time', 'value']]
        allowed_codes = ['switch_led', 'bright_value_v2', 'temp_value_v2', 'colour_data_v2']
        final_df.dropna(subset=['code', 'value'], inplace=True)
        final_df = final_df[final_df['code'].isin(allowed_codes)]

        return final_df

    def predict(self, df):
        df['event_time'] = pd.to_datetime(df['event_time'])
        df = df.sort_values(by=['device_id', 'code', 'event_time'])
        df['time'] = df['event_time'].dt.time
        df['ds'] = df['event_time'].dt.date + pd.to_timedelta(df['event_time'].dt.hour, unit='h') + pd.to_timedelta(df['event_time'].dt.minute, unit='m')

        result = []
        for device_id in df['device_id'].unique():
            for code in df['code'].unique():
                df_filtered = df[(df['device_id'] == device_id) & (df['code'] == code)].copy()
                df_filtered['value'] = df_filtered['value'].astype(str).str.replace("true", '1', regex=False).str.replace('false', '0', regex=False)
                if code == 'colour_data_v2':
                    df_filtered['value'] = df_filtered['value'].apply(self.hex_to_rgb)
                else:
                    df_filtered['value'] = pd.to_numeric(df_filtered['value'])
                df_filtered['value'] = pd.to_numeric(df_filtered['value'])
                if df_filtered.shape[0] < 2:
                    continue

                model = Prophet()
                model.fit(df_filtered[['ds', 'value']].rename(columns={'value': 'y'}))

                future_df = model.make_future_dataframe(periods=24 * 60, freq='T')

                future_df['time'] = df_filtered['time'].iloc[0]
                future_df['ds'] = pd.to_datetime(future_df['ds'].dt.date.astype(str) + ' ' + future_df['time'].astype(str))

                forecast = model.predict(future_df)

                next_day_start = df_filtered['ds'].max() + timedelta(days=1)
                next_day_end = next_day_start + timedelta(days=1)

                next_day_start = pd.to_datetime(next_day_start)
                next_day_end = pd.to_datetime(next_day_end)

                next_day_forecast = forecast[(forecast['ds'] >= next_day_start) & (forecast['ds'] < next_day_end)]

                for index, row in next_day_forecast.iterrows():
                    time_str = row['ds'].time().strftime('%H:%M')
                    predicted_value = row['yhat']

                    if code == 'switch_led':
                        value = True if predicted_value >= 0.5 else False
                    elif code == 'colour_data_v2':
                        rgb_value = max(0, min(int(predicted_value * 3), 765))
                        r, g, b = rgb_value // 256, (rgb_value % 256) // 16, rgb_value % 16
                        value = f"{r:02x}{g:02x}{b:02x}"
                        value = self.hex_to_hsv(value)
                    elif code == 'bright_value_v2':
                        value = max(0, min(int(predicted_value), 1000))
                    elif code == 'temp_value_v2':
                        value = max(0, min(int(predicted_value), 1000))
                    else:
                        value = predicted_value

                    result.append({
                        'device_id': device_id,
                        'code': code,
                        'time': time_str,
                        'value': value
                    })

        return result

    def format_predictions(self, predictions):
        merged_predictions = {}
        result = []

        for prediction in predictions:
            key = (prediction["time"], prediction["device_id"])
            if key not in merged_predictions:
                merged_predictions[key] = {
                    "alias_name": "".join(random.choices(string.ascii_letters + string.digits, k=15)),
                    "enable": True,
                    "time": prediction["time"],
                    "timezone_id": str(get_localzone()),
                    "category": "smart_mode",
                    "devices_timers": {prediction["device_id"]: ""},
                    "date": datetime.now().strftime("%Y%m%d"),
                    "functions": []
                }

            if prediction["code"] == "switch_led":
                code = "switch_led"
            elif prediction["code"] == "bright_value_v2":
                code = "bright_value"
            elif prediction["code"] == "temp_value_v2":
                code = "temp_value"
            elif prediction["code"] == "colour_data_v2":
                code = "colour_data"

            merged_predictions[key]["functions"].append({"code": code, "value": prediction["value"]})

        for key, value in merged_predictions.items():
            result.append(value)

        for item in result:
            if "switch_led" in item["functions"] and item["functions"]["switch_led"] is False:
                item["functions"] = {"switch_led": item["functions"]["switch_led"]}

        return result

    def hex_to_hsv(self, hex_str):
        if not hex_str:
            return {'h': 0, 's': 0, 'v': 0}

        hex_str = hex_str.lstrip('0x')

        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str

        try:
            r, g, b = tuple(int(hex_str[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            return {
                'h': round(h * 360, 2),
                's': round(s * 1000, 2),
                'v': round(v * 1000, 2)
            }
        except ValueError:
            return {'h': 0, 's': 0, 'v': 0}

    def hex_to_rgb(self, hex_str):
        if not hex_str:
            return 0
        hex_str = hex_str.lstrip('0x')

        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str

        try:
            r, g, b = tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
            return (r + g + b) / 3
        except ValueError:
            return 0
