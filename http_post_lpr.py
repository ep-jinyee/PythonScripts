import csv
import requests
import sys
import time
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def login_and_get_token(ip):
    """Log in to the API and retrieve the token from the cookie."""
    url = f"https://{ip}/token"
    payload = {
        "payload": {
            "username": "admin",
            "password": "123456"
        }
    }
    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes

        # Extract the token from the cookie
        if "k" in response.cookies:
            token = response.cookies["k"]
            print("Login successful! Token retrieved.")
            return token
        else:
            print("Error: Token not found in the response cookies.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        sys.exit(1)

def logout_and_remove_token(ip, token):
    """Log out and remove the token from the server."""
    url = f"https://{ip}/remove"
    cookies = {"k": token}  # Include the token in the cookies
    try:
        response = requests.get(url, cookies=cookies, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Logout successful! Token removed from the server.")
    except requests.exceptions.RequestException as e:
        print(f"Error during logout: {e}")
        sys.exit(1)

def send_api_request(car_plate, card_number, ip, token):
    # Construct the payload for the POST request
    payload = {
        "payload": [
            {"lpr": car_plate, "card": card_number}
        ]
    }

    cookies = {"k": token}
    # Send the POST request
    try:
        response = requests.post(f'https://{ip}/api/lpr', json=payload, cookies=cookies, verify=False)
        
        # Check for a successful request
        if response.status_code == 200:
            print(f"Successfully posted data for car plate: {car_plate}")
        else:
            print(f"Failed to post data for car plate: {car_plate}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending request for car plate {car_plate}: {e}")

def get_api_request(last_send_car_plate, card_no, ip, token):
    # Send the POST request
    cookies = {"k" : token}
    try:
        response = requests.get(f'https://{ip}/api/lpr?car_plate={last_send_car_plate}', cookies=cookies, verify=False)
        
        # Check for a successful request
        if response.status_code == 200:
            print(f"Successfully get data for car plate: {last_send_car_plate}")
            print(response.content)
            print(card_no)
        else:
            print(f"Failed to get data for car plate: {last_send_car_plate}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending request for car plate {last_send_car_plate}: {e}")
        exit()

if __name__ == "__main__":
    ip = '192.168.4.98'
    # Replace 'your_file.csv' with your actual CSV file path
    csv_file_path = "./resources/mockdata.csv"

    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        
        counter = 1 
        car_plate = ""
        card_number = ""

        # Process each row
        start_time = time.time()
        for row in reader:

            counter = counter + 1

            # Do halfway so skip those already done
            # if counter < 6960:
            #    continue 
            try:
                if len(row) >= 2:  # Ensure there are at least two columns in the row
                    car_plate = row[0].strip()
                    card_number = row[1].strip()
        
                    token = login_and_get_token(ip)
                    
                    send_api_request(car_plate, card_number, ip, token)

                    get_api_request(car_plate, card_number, ip, token)

                    logout_and_remove_token(ip, token)
            except Exception as e:
                print(e)
                sys.exit(1)
        
        spent = time.time() - start_time
        print(f"Spent time {spent}")