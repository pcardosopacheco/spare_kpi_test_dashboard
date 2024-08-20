import os
import requests
import logging
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Logging
log_filename = "fetch_data_log.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])

CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_data(url, data_type):
    """
    Fetch data from the Spare API and return as a list of dict.
    """
    token = os.getenv('SPARELABS_API_TOKEN')
    if not token:
        raise ValueError("API token is missing, set the token in the .env file.")

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    all_data = []

    # Fetch data page by page until all data is retrieved
    page = 1
    while True:
        params = {'limit': 50, 'skip': (page - 1) * 50}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            logging.error(f"Failed to fetch {data_type} data: {response.status_code} - {response.text}")
            response.raise_for_status()

        data = response.json()
        if not data or 'data' not in data:
            break

        all_data.extend(data['data'])

        # Log progress
        logging.info(f"Fetched {len(all_data)} {data_type} so far...")

        # If there are less than 50 records in the response, it means all data is fetched
        if len(data['data']) < 50:
            break

        page += 1

    logging.info(f"Fetched {len(all_data)} {data_type}.")
    return all_data

def fetch_ridership_data():
    cache_file = os.path.join(CACHE_DIR, 'ridership_data.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    else:
        url = "https://api.sparelabs.com/v1/exports/ridership"
        data = fetch_data(url, "ridership")
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return data

def fetch_duty_data():
    cache_file = os.path.join(CACHE_DIR, 'duty_data.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    else:
        url = "https://api.sparelabs.com/v1/exports/driverReport"
        data = fetch_data(url, "duty")
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return data

if __name__ == "__main__":
    ridership_data = fetch_ridership_data()
    duty_data = fetch_duty_data()
