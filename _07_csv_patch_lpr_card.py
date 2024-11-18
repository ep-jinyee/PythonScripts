import csv
import requests

# Configuration
CSV_FILE = "car_plate_data.csv"  # Replace with your actual CSV file path
API_ENDPOINT = "https://192.168.88.124/api/lpr"  # Replace with your endpoint URL
CARD_NUMBER = "1230000000"

def send_patch_request(car_plate):
    """Sends a PATCH request with the given car plate."""
    payload = {
        "payload": {
            "lpr": car_plate,
            "card": CARD_NUMBER
        }
    }
    try:
        response = requests.patch(API_ENDPOINT, json=payload)
        if response.status_code == 200:
            print(f"Successfully updated card number for {car_plate}.")
        else:
            print(f"Failed to update {car_plate}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending request for {car_plate}: {e}")

def main():
    """Main function to read the CSV and send PATCH requests."""
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if it exists
        for row in reader:
            car_plate = row[0].strip()
            send_patch_request(car_plate)

if __name__ == "__main__":
    main()
