from scapy.all import Ether, sendp

# Define the destination MAC address and source MAC address
dst_mac = "88:97:DF:11:22:55"  # Replace with your target MAC address
src_mac = "66:77:88:99:AA:BB"  # Replace with your source MAC address

# Create an Ethernet frame (Layer 2)
ethernet_frame = Ether(dst=dst_mac, src=src_mac)

# Optionally, you can add a payload (for example, raw data)
payload = b"Hello, Layer 2!"  # This is raw data you can send
packet = ethernet_frame / payload  # Combine Ethernet frame with payload

# Send the packet
sendp(packet, iface="eth0")  # Replace "eth0" with your network interface name
