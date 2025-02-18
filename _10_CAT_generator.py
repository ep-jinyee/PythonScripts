import random
import string
import struct

def generate_random_string(length=10):
    """Generate a random string of fixed length"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_data(num_entries=20000):
    """Generate random data for num_entries, each entry occupies 16 bytes"""
    data = []
    
    for _ in range(num_entries):
        # Generate a random string of 10 characters (12 bytes, including padding)
        random_str = generate_random_string()
        # Pad it to 12 bytes (if necessary)
        random_str = random_str.ljust(12, '0')
        
        # Generate a random 4-byte integer (uint32_t)
        random_int = random.randint(0, 0xFFFFFFFF)
        
        # Create the 16-byte entry (12 bytes string + 4-byte integer)
        entry = random_str.encode('utf-8') + struct.pack('I', random_int)
        
        # Append the entry to the data list
        data.append(entry)
    
    return data

def save_to_file(filename, data):
    """Save the data to a file"""
    with open(filename, 'wb') as f:
        for entry in data:
            f.write(entry)

if __name__ == '__main__':
    # Generate random data for 20,000 entries
    random_data = generate_random_data(20000)
    
    # Save the data to CAT.TXT
    save_to_file('CAT.TXT', random_data)

    print(f"Successfully generated {len(random_data)} entries and saved to CAT.TXT.")
