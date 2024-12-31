# send_to_splunk.py

import json
import requests
import sys

# Splunk HEC credentials (hardcoded)
SPLUNK_URL = 'https://http-inputs-remitly.splunkcloud.com/services/collector/event'
SPLUNK_TOKEN = 'b8eb4e10-6ea8-4c26-a296-0dfd96c401c7'

def send_to_splunk_event(json_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            json_str = file.read()

        # Parse the JSON event
        data = json.loads(json_str)

        # Wrap the JSON object inside 'event'
        payload = {"event": data}

        # Convert the payload to string
        payload_str = json.dumps(payload)

        # Set headers for the HTTP request
        headers = {
            'Authorization': f'Splunk {SPLUNK_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Send the data to Splunk
        response = requests.post(SPLUNK_URL, headers=headers, data=payload_str)

        # Check the response from Splunk
        if response.status_code != 200:
            print(f"Failed to send data to Splunk. Status code: {response.status_code}")
            print(response.text)
        else:
            print("Successfully sent data to Splunk.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 send_to_splunk.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    send_to_splunk_event(json_file_path)