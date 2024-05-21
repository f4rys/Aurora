import os
from datetime import datetime, timedelta
import random
import string
import colorsys

from tzlocal import get_localzone

import pandas as pd
from prophet import Prophet


class TuyaSmartMode():
    def __init__(self):
        self.predictions = []

    def hex_to_hsv(self, hex_str):
        """Converts a hexadecimal color string to HSV, handling empty strings and invalid hex formats."""
        if not hex_str:  # Handle empty strings
            return {'h': 0, 's': 0, 'v': 0}
        
        hex_str = hex_str.lstrip('0x')

        #Ensure that the string is of even length representing valid hex pairs
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str

        try:
            r, g, b = tuple(int(hex_str[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            return {
                'h': round(h * 360, 2),  # Rescale to 0-360
                's': round(s * 1000, 2), # Rescale to 0-1000
                'v': round(v * 1000, 2)  # Rescale to 0-1000
            }  # Return as dictionary
        except ValueError:  # Handle invalid hex format
            return {'h': 0, 's': 0, 'v': 0}

    def hex_to_rgb(self, hex_str):
        """Converts a hexadecimal color string to an average RGB value, 
        handling empty strings and invalid hex formats."""
        if not hex_str:  # Handle empty strings
            return 0  
        hex_str = hex_str.lstrip('0x')

        #Ensure that the string is of even length representing valid hex pairs
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str

        try:
            r, g, b = tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
            return (r + g + b) / 3
        except ValueError:  # Handle invalid hex format
            return 0

    def create_dataframe(self):
        directory = 'modules/resources/json/logs'
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

        # Process each file and store the DataFrames
        dfs = []
        for file in json_files:
            file_path = os.path.join(directory, file)
            df = pd.read_json(file_path)
            df['device_id'] = os.path.basename(file_path).split('.')[0]  # Extract device_id from filename
            dfs.append(df)

        # Combine all DataFrames
        final_df = pd.concat(dfs, ignore_index=True)

        # Select relevant columns
        final_df = final_df[['device_id', 'code', 'event_time', 'value']]
        allowed_codes = ['switch_led', 'bright_value_v2', 'temp_value_v2', 'colour_data_v2']
        final_df.dropna(subset=['code', 'value'], inplace=True)
        final_df = final_df[final_df['code'].isin(allowed_codes)]

        # Display the first 5 rows
        return final_df

    def train_model(self):
        df = self.create_dataframe()
        predicted_actions = self.train_and_predict(df)
        formatted_predictions = self.format_and_save_output(predicted_actions)
        print(formatted_predictions)

    def train_and_predict(self, df):
        # Data Preparation
        df['event_time'] = pd.to_datetime(df['event_time'])  # Convert to datetime
        df = df.sort_values(by=['device_id', 'code', 'event_time'])  # Sort data
        # Create new columns for time and date for future predictions
        df['time'] = df['event_time'].dt.time
        df['ds'] = df['event_time'].dt.date + pd.to_timedelta(df['event_time'].dt.hour, unit='h') + pd.to_timedelta(df['event_time'].dt.minute, unit='m')

        # Initialize result list
        result = []

        # Iterate through devices and codes
        for device_id in df['device_id'].unique():
            for code in df['code'].unique():
                df_filtered = df[(df['device_id'] == device_id) & (df['code'] == code)].copy()
                df_filtered['value'] = df_filtered['value'].astype(str).str.replace("true", '1', regex=False).str.replace('false', '0', regex=False)
                if code == 'colour_data_v2':
                    df_filtered['value'] = df_filtered['value'].apply(self.hex_to_rgb)
                else:
                    df_filtered['value'] = pd.to_numeric(df_filtered['value'])
                df_filtered['value'] = pd.to_numeric(df_filtered['value'])
                if df_filtered.shape[0] < 2:  # Prophet needs at least 2 data points
                    continue
                # Model Building
                model = Prophet()
                model.fit(df_filtered[['ds', 'value']].rename(columns={'value': 'y'}))
                
                # Create a dataframe for future dates
                future_df = model.make_future_dataframe(periods=24 * 60, freq='T')  # Predictions for every minute in the next day

                # Add the time component from the original data to the future dataframe
                future_df['time'] = df_filtered['time'].iloc[0]  # Use the first time value from the filtered data
                future_df['ds'] = pd.to_datetime(future_df['ds'].dt.date.astype(str) + ' ' + future_df['time'].astype(str))

                # Forecasting
                forecast = model.predict(future_df)

                # Extract next day predictions
                next_day_start = df_filtered['ds'].max() + timedelta(days=1)
                next_day_end = next_day_start + timedelta(days=1)

                # Convert next_day_start and next_day_end to datetime for proper comparison
                next_day_start = pd.to_datetime(next_day_start)  
                next_day_end = pd.to_datetime(next_day_end)  

                next_day_forecast = forecast[(forecast['ds'] >= next_day_start) & (forecast['ds'] < next_day_end)]

                for index, row in next_day_forecast.iterrows():
                    time_str = row['ds'].time().strftime('%H:%M')
                    predicted_value = row['yhat']  # Get the predicted value

                    # Apply transformation based on the code
                    if code == 'switch_led':
                        value = True if predicted_value >= 0.5 else False
                    elif code == 'colour_data_v2':
                        rgb_value = max(0, min(int(predicted_value * 3), 765)) # Scale and clamp to valid RGB range
                        r, g, b = rgb_value // 256, (rgb_value % 256) // 16, rgb_value % 16
                        value = f"{r:02x}{g:02x}{b:02x}"  # Convert to hexadecimal string
                        value = self.hex_to_hsv(value)
                    elif code == 'bright_value_v2':
                        value = max(0, min(int(predicted_value), 1000)) # Clamp to 0-1000 range
                    elif code == 'temp_value_v2':
                        value = max(0, min(int(predicted_value), 1000)) # Clamp to 0-1000 range
                    else:
                        value = predicted_value  # Keep as is for other codes

                    result.append({
                        'device_id': device_id,
                        'code': code,
                        'time': time_str,
                        'value': value
                    })

        return result 

    def format_and_save_output(self, predictions):
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
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "functions": {}
                }
            merged_predictions[key]["functions"][prediction["code"]] = prediction["value"]

        for key, value in merged_predictions.items():
            result.append(value)

        for item in result:
            if "switch_led" in item["functions"] and item["functions"]["switch_led"] == False:
                item["functions"] = {"switch_led": item["functions"]["switch_led"]}

        return result