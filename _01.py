#! /usr/bin/python3
import requests
import random
import string
import argparse
import json

out_dir = 'lpr.txt'

session = requests.Session()

# Step 1: Authenticate and retrieve API token (assumed to be returned in the cookie)
login_url = "https://192.168.88.125/api"
login_data = {
    {
        "payload": {
            "username": "admin", 
            "password": "123456"
        }
    }
}

# Function to generate random Malaysian car plate numbers
def generate_lpr():
    # Car plates in Malaysia generally have letters followed by numbers (e.g., ABC1234)
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))  # 3 random uppercase letters
    numbers = ''.join(random.choices(string.digits, k=4))           # 4 random digits
    return f"{letters}{numbers}"

# Function to generate random card number (10 digits, starting with '1')
def generate_card():
    return '1' + ''.join(random.choices(string.digits, k=9))

# Generate 10,000 data
def generate_payload(num_records=10000):
    data = []
    for _ in range(num_records):
        lpr = generate_lpr()
        card = generate_card()
        data.append({"lpr": lpr, "card": card})
    return data

# Function to append data to lpr.txt in bytes
def append_to_file(car_plate, card_number):
    with open(out_dir, 'ab') as f:  # 'ab' mode for appending in binary
        f.write(car_plate.encode('utf-8').rjust(18, b'\x30') + int(card_number).to_bytes(4, byteorder='big', signed=False))

# Function to send data in batches of 10
def send_data_to_api(endpoint_url, payload, batch_size=10):
    # Split data into batches of 10
    for i in range(0, len(payload), batch_size):
        batch = payload[i:i + batch_size]
        request_payload = {"payload": batch}
        try:
            response = requests.post(endpoint_url, json=request_payload, verify=False)
            # Handle response
            if response.status_code == 200:
                print(f"Batch {i // batch_size + 1}: Success")
                # Append car plates and card numbers to the file in bytes
                for item in batch:
                    append_to_file(item['lpr'], item['card'])
            else:
                print(f"Batch {i // batch_size + 1}: Failed with status code {response.status_code}")

        except requests.RequestException as e:
            print(f"Batch {i // batch_size + 1}: Error occurred - {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI tool to generate and send random LPR and card data to an API.")
    
    # Add arguments for API endpoint and number of records
    parser.add_argument('--endpoint', type=str, help="IP address to send data", required=True)
    parser.add_argument('--num_records', type=int, help="Number of random data records to generate", required=True)
    parser.add_argument('--out_dir', type=int, help="Output directory of lpr.txt, default is same directory as where this program is invoked", required=False)

    # Parse command-line arguments
    args = parser.parse_args()

    # Login request to get the token in the cookie
    response = session.post(login_url, json=login_payload)

    # Check if login was successful
    if response.status_code == 200:
        print("Login successful")
        print("Cookies after login:", session.cookies.get_dict())
        protected_url = "https://" + argps.endpoint + "/api/lpr"

        # Generate data and send to the API
        data = generate_payload(args.num_records)
        send_data_to_api(protected_url, data)
    else:
        print(f"Login failed. Status code: {response.status_code}")

# Example usage
if __name__ == "__main__":
    main()
    
