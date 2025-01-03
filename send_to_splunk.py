# send_to_splunk.py

import json
import requests
import sys

# Splunk HEC credentials (hardcoded)

def send_to_splunk_event(json_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            lines = file.readlines()  # Read all lines (assuming JSON lines format)

        for line in lines:
            # Parse each JSON line
            try:
                data = json.loads(line.strip())  # Parse a single JSON object
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {e}")
                continue

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

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 send_to_splunk.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    send_to_splunk_event(json_file_path)
