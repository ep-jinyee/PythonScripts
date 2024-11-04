import serial
import time

def main():
    # Configure the serial port
    port = 'COM3'
    baud_rate = 9600  # Adjust based on your device's requirements
    interval = 8      # Time between transmissions in seconds
    car_plates = [
        'JLR8',
        'TCC555',
        'ABC123',
        'WQQ4595',
        'QAL4',
        'WYP181',
        'MALAYSIA38',
        'PATRIOT1200',
        'MALAYSIA9988',
        'ANBU99W',
        'HEHE99',
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

                data = header + bytes([plate_length]) + bytes([0x01, 0x0A, 0x01, 0x00]) + plate + footer

                # Send the data
                ser.write(data)
                print(f"Sent: {data.hex()}")

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
