import requests
import random
import string
import json

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
            else:
                print(f"Batch {i // batch_size + 1}: Failed with status code {response.status_code}")

        except requests.RequestException as e:
            print(f"Batch {i // batch_size + 1}: Error occurred - {e}")

# Example usage
if __name__ == "__main__":
    api_endpoint = "https://192.168.88.122/api/lpr"  # Replace with your actual API endpoint
    data = generate_payload(10)  # Generate 10,000 data points
    send_data_to_api(api_endpoint, data)
