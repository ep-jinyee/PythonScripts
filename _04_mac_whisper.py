#!/usr/bin/env python
import argparse
import fcntl
import json
import re
import signal
import socket
import struct
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

KEEP_RUNNING = True
EDGE_MAC = ""


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        if re.search('/api/confirm-config/', self.path):
            length = int(self.headers.get('Content-Length'))
            payload = self.rfile.read(length).decode('utf8')
            payload_dict = json.loads(payload)

            if payload_dict.get("mac"):
                payload_mac = payload_dict.get("mac")
                if payload_mac == EDGE_MAC:
                    print(payload)
                    self.send_response(200)
                    self.server.server_close()
                    globals()['KEEP_RUNNING'] = False
                else:
                    self.send_response(403)
            else:
                self.send_response(403)
        else:
            self.send_response(403)

        self.end_headers()


def send_frame(ifname, dstmac, eth_type, payload):
    # Open raw socket and bind it to network interface.
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((ifname, 0))

    # Get source interface's MAC address.
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    srcmac = ':'.join('%02x' % b for b in info[18:24])

    # Build Ethernet frame
    payload_bytes = payload.encode('utf-8')
    assert len(payload_bytes) <= 1500  # Ethernet MTU

    frame = convert_mac_to_bytes(dstmac) + convert_mac_to_bytes(srcmac) + eth_type + payload_bytes

    # Send Ethernet frame
    return s.send(frame)


def convert_mac_to_bytes(addr):
    return bytes.fromhex(addr.replace(':', ''))


def start_web_server():
    global KEEP_RUNNING

    server = HTTPServer(('0.0.0.0', 18080), HTTPRequestHandler)
    try:
        while KEEP_RUNNING:
            server.handle_request()

        if not KEEP_RUNNING:
            sys.exit(0)

    except KeyboardInterrupt:
        pass
    except Exception as error:
        return
    server.server_close()


def handle_timeout(sig, frame):
    sys.exit(3)


def main():
    global EDGE_MAC

    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', type=str, help='Network interface', required=True)
    parser.add_argument('--dst-mac', type=str, help='Destination MAC Address', required=True)
    parser.add_argument('--payload', type=str, help='JSON Payload', required=True)
    parser.add_argument('--timeout', type=int, default=2, help='Timeout of the process')
    args = parser.parse_args()

    ifname = args.interface
    dstmac = args.dst_mac
    payload = args.payload
    ethtype = b'\x69\x69'

    # Send frame to Edge
    try:
        send_frame(ifname, dstmac, ethtype, payload)
    except Exception as error:
        print(error)
        sys.exit(1)

    # Start webserver with timeout
    EDGE_MAC = args.dst_mac
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(args.timeout)
    start_web_server()


if __name__ == "__main__":
    main()
