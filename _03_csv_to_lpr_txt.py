import csv
import struct

def convert_csv_to_lpr(csv_filename, output_filename):
    with open(csv_filename, 'r') as csv_file, open(output_filename, 'wb') as output_file:
        reader = csv.reader(csv_file)
        rows_written = 0
        
        for row in reader:
            car_plate, card_no = row
            
            # Pad car plate to 20 characters with '0's if necessary
            padded_car_plate = car_plate.zfill(20)
            
            # Convert car plate to bytes (ASCII encoding)
            car_plate_bytes = padded_car_plate.encode('ascii')
            
            # Convert card number to uint32_t in 4-byte format
            card_number = int(card_no)
            card_bytes = struct.pack('<I', card_number)  # Big-endian uint32_t
            
            # Write to the output file
            output_file.write(car_plate_bytes)
            output_file.write(card_bytes)

            rows_written += 1

        # rows_needed = 10000 - rows_written

        # for _ in range(rows_needed):
            # output_file.write(b'\xFF' * 24)

# Example usage
convert_csv_to_lpr('./resources/mockdata.csv', './results/lpr.txt')
