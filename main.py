# import argparse

# def main():
#   parse = argparse.ArgumentParser(description="A CLI program that bundles a handful of useful utilities created by JY")

import argparse
from colorama import Fore, Back, Style, init
import pyfiglet
import sys

# Initialize Colorama for cross-platform support
init()

def print_welcome_message():
    ascii_art = pyfiglet.figlet_format("Welcome to My Test App!")
    print(Fore.CYAN + ascii_art)  # Fancy ASCII art in cyan
    print(Fore.YELLOW + "Let's run some tests on the Device Under Test (DUT).")
    print(Style.BRIGHT + "Use --help for available commands and options." + Style.RESET_ALL)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CLI Test Software")
    parser.add_argument(
        "--dut_ip", 
        type=str, 
        help="IP address of the DUT device."
    )
    parser.add_argument(
        "--num_plates", 
        type=int, 
        help="Number of car plates to generate."
    )
    args = parser.parse_args()

    # If no arguments are passed, show the welcome screen
    if len(sys.argv) == 1:
        print_welcome_message()

    # Otherwise, proceed with the rest of the functionality
    else:
        if args.dut_ip and args.num_plates:
            print(f"Running tests on DUT at {args.dut_ip} with {args.num_plates} car plates.")
        else:
            print("Missing arguments. Use --help for more details.")

if __name__ == "__main__":
    main()
