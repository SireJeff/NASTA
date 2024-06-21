import requests
import json
import schedule
import time
from pprint import pprint
from datetime import datetime, timedelta

# An API key is required to access the Neo API. Get your API key from: https://api.nasa.gov/
api_key = ''

def get_neo_data():
    # Specify the start and end dates for the day it's being run
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={current_date}&end_date={current_date}&api_key={api_key}'

    # Making a request and getting data
    r = requests.get(url)
    data = r.json()
    print(current_date)
    
    # Extracting asteroid data
    neo = data['near_earth_objects'][current_date]
    
    # Print or process the NEO data as needed
    #print(data)
    for near in neo:
        print(f"{near['id']}, {near['name']}, {near['close_approach_data'][0]['close_approach_date_full']}\n")

        # Additional processing...

# Define the job to be run in 1 minute from now
start_time = datetime.now() + timedelta(minutes=1)
start_hour = start_time.hour
start_minute = start_time.minute

job_time = f"{start_hour:02d}:{start_minute:02d}"
print(f"Job scheduled at: {job_time}")
schedule.every(100).seconds.do(get_neo_data)

# Run the job continuously
while True:
    print("Checking for scheduled jobs...")
    schedule.run_pending()
    time.sleep(1)
