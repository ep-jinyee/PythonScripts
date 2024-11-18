import csv
import requests

# Configuration
CSV_FILE = "car_plate_data.csv"  # Replace with your actual CSV file path
API_ENDPOINT = "https://192.168.88.247/api/lpr"  # Replace with your endpoint URL

def send_delete_request(car_plate):
    """Sends a DELETE request with the given car plate as a query parameter."""
    params = {"car_plate": car_plate}
    try:
        response = requests.delete(API_ENDPOINT, params=params)
        if response.status_code == 200:
            print(f"Successfully deleted entry for {car_plate}.")
        else:
            print(f"Failed to delete {car_plate}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending request for {car_plate}: {e}")

def main():
    """Main function to read the CSV and send DELETE requests."""
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if it exists
        for row in reader:
            car_plate = row[0].strip()
            send_delete_request(car_plate)

if __name__ == "__main__":
    main()
