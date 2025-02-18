import serial
import time

def main():
    # Configure the serial port
    port = 'COM7'
    baud_rate = 9600  # Adjust based on your device's requirements
    interval = 1      # Time between transmissions in seconds
    car_plates = [
        'JLR8',
        'DEE51',
        'WXQ3411',
        'MAK6',
        'LF6999',
        'MCR66',
        'CT13',
        'TCC555',
        'BHN2812',
        'BLU1837',
        'DDQ8888',
        'BJG2288',
        'JTT8888',
        'QAL4',
        'TAN6682',
        'VDJ9',
        'WVR28',
        'W8237K',
        'WYP181',
        'VAA7877',
        'RIMAU3318',
        'MALAYSIA38',
        'VBR1102',
        'PATRIOT1200',
        'MALAYSIA9988',
        'VEJ3033',
        'VFN1280',
        'WC2005F',
        'WQQ4595',
        'WWT5726'
        'ANBU99W',
        "_NONE_",
        "No_Plate",
        'CHAN123',
        'BENSON456'
    ]

    try:
        # Open the serial port
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            print(f"Connected to {port}")
            i = 0
            while True:
                # Construct the data packet
                header = bytes([0xaa, 0x55, 0x00, 0x64, 0x00, 0x27, 0x00])
                plate = car_plates[i].encode('ascii')
                plate_length = len(plate) + 4
                footer = bytes([0x00, 0x00, 0xaf])

                # data = header + bytes([plate_length]) + bytes([0x01, 0x0A, 0x01, 0x00]) + plate + footer
                # data = data + (header + bytes([plate_length]) + bytes([0x01, 0x0A, 0x01, 0x00]) + plate + footer)
                # data = header + bytes([0]) + bytes([0x01, 0x0A, 0x01, 0x00])  + "".encode('ascii') + footer
                # data += (header + bytes([plate_length]) + bytes([0x01, 0x0A, 0x01, 0x00]) + plate + footer)
                data = (header + bytes([plate_length]) + bytes([0x01, 0x00, 0x01, 0x00]) + plate + footer)
                ser.write(data)
                print(f"Sent: {data.hex()}")
                time.sleep(0.1)

                data = (header + bytes([0x00, plate_length]) + bytes([0x01, 0x00, 0x02, 0x00]) + plate + footer)
                ser.write(data)
                print(f"Sent: {data.hex()}")
                time.sleep(0.1)

                data = (header + bytes([0x00, len("Slow down")]) + bytes([0x01, 0x00, 0x03, 0x00]) + "Slow down".encode('ascii') + footer)
                ser.write(data)
                print(f"Sent: {data.hex()}")
                time.sleep(0.1)

                data = (header + bytes([0x00, len("Welcome to Entrypass")]) + bytes([0x01, 0x00, 0x04, 0x00]) + "Welcome to Entrypass".encode('ascii') + footer)
                ser.write(data)
                print(f"Sent: {data.hex()}")
                time.sleep(0.1)

                # Move to the next plate
                i = (i + 1) % len(car_plates)

                # Wait for the specified interval
                time.sleep(interval)

    except serial.SerialException as e:
        print(f"Error with serial port {port}: {e}")
    except KeyboardInterrupt:
        print("Transmission stopped by user.")

if __name__ == "__main__":
    main()
