import csv
import struct
import sys
import os
import argparse
import ipaddress
import requests
from datetime import datetime

glb_token = ""

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

def download_lpr_file(ip, token, destination_dir):
    """Download the LPR file from the specified IP address using the token."""
    url = f"https://{ip}/api/lpr/file"
    cookies = {"k": token}  # Include the token in the cookies
    try:
        response = requests.get(url, cookies=cookies, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        lpr_file_path = os.path.join(destination_dir, "tmp.txt")
        with open(lpr_file_path, 'wb') as file:
            file.write(response.content)
        print(f"LPR file downloaded successfully to: {lpr_file_path}")
        return lpr_file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading LPR file: {e}")
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

def convert_lpr_to_csv(lpr_filename, output_csv_filename):
    """Convert the LPR file to a CSV file."""
    with open(lpr_filename, 'rb') as lpr_file, open(output_csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        while True:
            # Read 20 bytes for the car plate and 4 bytes for the card number
            car_plate_bytes = lpr_file.read(20)
            card_bytes = lpr_file.read(4)

            if not car_plate_bytes or not card_bytes:
                break  # End of file

            # Convert car plate bytes back to a string (ASCII encoding)
            car_plate = car_plate_bytes.rstrip(b'\xFF').decode('ascii', errors='ignore')  # Remove padding and decode

            # Convert card bytes back to an unsigned int
            card_number = struct.unpack('<I', card_bytes)[0]  # Little-endian uint32_t

            # Write the extracted values to the CSV file
            writer.writerow([car_plate, card_number])

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert .lpr files to CSV.")
    parser.add_argument('--ip', type=str, help="Valid IP address for processing.")
    parser.add_argument('--destination', type=str, default=os.getcwd(), help="Destination directory for the output CSV file (default: current directory).")

    args = parser.parse_args()

    # Validate the IP address
    try:
        ipaddress.ip_address(args.ip)
    except ValueError:
        print("Error: Invalid IP address provided.")
        sys.exit(1)

    # Ensure the destination directory exists
    os.makedirs(args.destination, exist_ok=True)

    # Log in and get the token
    token = login_and_get_token(args.ip)

    # Download the LPR file using the token
    lpr_file_path = download_lpr_file(args.ip, token, args.destination)

    # Convert the .lpr file to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_filename = os.path.join(args.destination, f'result_{args.ip}_{timestamp}.csv')

    try:
        convert_lpr_to_csv(lpr_file_path, output_csv_filename)
        print(f"Conversion successful! CSV file saved to: {output_csv_filename}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
    finally:
        # Log out and remove the token
        logout_and_remove_token(args.ip, token)
        glb_token = ""
        if (os.path.exists("tmp.txt")):
            os.remove("tmp.txt")


if __name__ == "__main__":
    main()