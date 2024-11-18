import csv
import requests

# Replace with your actual endpoint URL
endpoint_url = "https://192.168.88.247/api/lpr"

def send_api_request(car_plate, card_number):
    # Construct the payload for the POST request
    payload = {
        "payload": [
            {"lpr": car_plate, "card": card_number}
        ]
    }
    
    # Send the POST request
    try:
        response = requests.post(endpoint_url, json=payload, verify=False)
        
        # Check for a successful request
        if response.status_code == 200:
            print(f"Successfully posted data for car plate: {car_plate}")
        else:
            print(f"Failed to post data for car plate: {car_plate}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending request for car plate {car_plate}: {e}")

def process_csv(csv_file):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Skip header row if there is one (optional)
        # next(reader, None)
        
        # Process each row
        for row in reader:
            if len(row) >= 2:  # Ensure there are at least two columns in the row
                car_plate = row[0].strip()  # Assuming the first column is the car plate
                card_number = row[1].strip()  # Assuming the second column is the card number
                send_api_request(car_plate, card_number)

if __name__ == "__main__":
    # Replace 'your_file.csv' with your actual CSV file path
    csv_file_path = "lpr-10000.csv"
    process_csv(csv_file_path)
