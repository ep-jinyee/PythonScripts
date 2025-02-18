import random
import struct
import time

DEF_MAX_CARD_PIN = 3
DEF_PIN_BCD_LEN = 3
DEF_MAX_DOOR_ACCESS = 5

def generate_random_bcd(length):
    """Generate random BCD data (6 digits) in `length` bytes."""
    value = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return bytes(int(value[i:i + 2]) for i in range(0, len(value), 2))

def generate_card_info():
    """Generate a single S_CARD_INFO entry."""
    # type: random 0 or 1
    type_value = random.randint(0, 1)

    # start_time and end_time
    start_time = int(time.time()) + random.randint(0, 1000)
    end_time = start_time + random.randint(60, 3600)

    # pin[3][3]: 9 bytes BCD
    pin_data = b''.join(generate_random_bcd(3) for _ in range(DEF_MAX_CARD_PIN))

    # door_access[DEF_MAX_DOOR_ACCESS]: 10 bytes
    door_access = [random.randint(0, 0xFFFF) for _ in range(DEF_MAX_DOOR_ACCESS)]
    
    # curr_zone, status, pin_err_count: 1 byte each
    curr_zone = random.randint(0, 255)
    status = random.randint(0, 255)
    pin_err_count = random.randint(0, 255)

    # buddy_no: 2 bytes set to 0
    buddy_no = 0

    # misc[5]: filled with 0xFF
    misc = b'\xFF' * 5

    # Pack the data into 64 bytes using struct
    return struct.pack(
        '<BII9s5HBBHB5s',
        type_value, 
        start_time, 
        end_time, 
        pin_data, 
        *door_access, 
        curr_zone, 
        status, 
        pin_err_count, 
        buddy_no, 
        misc
    )

def generate_entries(num_entries=20000):
    """Generate multiple S_CARD_INFO entries."""
    entries = []
    for _ in range(num_entries):
        entries.append(generate_card_info())
    return b''.join(entries)

def save_to_file(filename, data):
    """Save binary data to a file."""
    with open(filename, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    # Generate the data and write it to CD.TXT
    binary_data = generate_entries(20000)
    save_to_file('CD.TXT', binary_data)
    print(f"Successfully generated and saved 20,000 entries to CD.TXT.")

