import csv
import requests

# Replace with your actual endpoint URL
endpoint_url = "https://192.168.4.155/api/lpr"

def send_api_request(car_plate, card_number):
    # Construct the payload for the POST request
    payload = {
        "payload": []
    }

    index = 0
    for c in car_plate:
        payload["payload"].append(
            {"lpr": c, "card": card_number[index]}
        )
        index = index + 1

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

def get_api_request(last_send_car_plate):
    # Send the POST request
    for cp in last_send_car_plate:
        try:
            response = requests.get(endpoint_url + '?car_plate=' + cp, verify=False)
            
            # Check for a successful request
            if response.status_code == 200:
                print(f"Successfully get data for car plate: {cp}")
            else:
                print(f"Failed to get data for car plate: {cp}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while sending request for car plate {cp}: {e}")
            exit()

def process_csv(csv_file):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        # Skip header row if there is one (optional)
        # next(reader, None)

        counter = 1 
        car_plate = []
        card_number = []

        # Process each row
        for row in reader:

            counter = counter + 1

            # Do halfway so skip those already done
            # if counter < 6960:
            #    continue 

            if len(row) >= 2:  # Ensure there are at least two columns in the row
                car_plate.append(row[0].strip())
                card_number.append(row[1].strip())

                if (counter % 20 == 0):
                    # last_send_car_plate = car_plate
                    send_api_request(car_plate, card_number)
                    # get_api_request(last_send_car_plate)
                    car_plate = []
                    card_number = []


if __name__ == "__main__":
    # Replace 'your_file.csv' with your actual CSV file path
    csv_file_path = "resources/skyvouge-10k.csv"
    process_csv(csv_file_path)
