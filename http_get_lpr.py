import pandas as pd
import random
import requests
import sys

# Load CSV file
def load_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    return df

# Select 50 unique random car plates and their associated card numbers
def get_random_carplates(df, num_samples=10000):
    sampled = df.sample(n=num_samples, random_state=None)
    return sampled.values.tolist()  # Convert to list of lists

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

# Query card number using car plate
def query_card_number(ip, car_plate, token):
    url = f"https://{ip}/api/lpr?car_plate={car_plate}"
    cookies = {"k": token}
    response = requests.get(url, cookies =cookies, verify=False)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("card")  # Adjusted according to payload structure
    
    # .get("card_number")  # Adjust according to API response
    return None

# Main function
def main():
    file_path = "./resources/mockdata.csv"  # Update with actual file path
    ip = "192.168.4.98"
    
    df = load_csv(file_path)
    carplate_data = get_random_carplates(df)
    
    for car_plate, expected_card_no in carplate_data:
        token = login_and_get_token(ip)

        queried_card_no = query_card_number(ip, car_plate, token)
        
        if queried_card_no == str(expected_card_no):
            print(f"MATCH: {car_plate} -> {expected_card_no}")
        else:
            print(f"MISMATCH: {car_plate} -> Expected {expected_card_no}, Got {queried_card_no}")
        
        logout_and_remove_token(ip, token)

if __name__ == "__main__":
    main()
