import csv
import struct

def convert_lpr_to_csv(lpr_filename, output_csv_filename):
    with open(lpr_filename, 'rb') as lpr_file, open(output_csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        while True:
            # Read 20 bytes for the car plate and 4 bytes for the card number
            car_plate_bytes = lpr_file.read(20)
            card_bytes = lpr_file.read(4)

            if not car_plate_bytes or not card_bytes:
                break  # End of file

            # Convert car plate bytes back to a string (ASCII encoding)
            car_plate = car_plate_bytes.rstrip(b'\xFF')  # Remove any padding zeros

            # Convert card bytes back to an unsigned int
            card_number = struct.unpack('<I', card_bytes)[0]  # Big-endian uint32_t

            # Write the extracted values to the CSV file
            writer.writerow([car_plate, card_number])

# Example usage
convert_lpr_to_csv('results\\dut_lpr.txt', 'results\\reversed_skyvouge.csv')
