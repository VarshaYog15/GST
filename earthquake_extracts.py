import requests
import pandas as pd
from datetime import datetime
from time import sleep

all_records = []

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

start_year = datetime.now().year - 5
end_year = datetime.now().year

print(f"\n Fetching earthquake data from {start_year} to {end_year}\n")


for year in range(start_year, end_year + 1):
    for month in range(1, 13):

        start_date = f"{year}-{month:02d}-01"


        if month == 12:
            end_date = f"{year+1}-01-01"

        else:
            end_date =f"{year}-{month+1:02d}-01"

        print(f"Requesting {start_date} - {end_date}")

        params = {
            "format": "geojson",
            "starttime" : start_date,
            "endtime" : end_date,
            "minmagnitude" : 1.0
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("API Error:", response.text[:200])
            continue

        print("Success")

        data = response.json()
        features = data.get("features", [])


        print(f"  - {len(features)} records found")
        all_records.extend(features)


        sleep(0.3)

df_raw = pd.json_normalize(all_records)
df_raw. to_csv("C:/Users/VARSHA/Documents/Python/py_venv/eq_raw.csv", index=False)

print("\nExtraction completed!")
print(f"Total records: {len(df_raw)}")
print("Saved to: output/eq_raw.csv")