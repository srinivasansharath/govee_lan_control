import socket
import struct
import json


def send_udp_packet(ip, port, payload):
    # Convert the JSON payload to bytes
    packet = json.dumps(payload).encode('utf-8')

    # Configure a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    try:
        sock.sendto(packet, (ip, port))
        #print(f"Sent message to {ip}:{port}:{packet}")
    finally:
        sock.close()


def receive_udp_packet(ip, port, time=1):
    # Configure a socket for receiving
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.bind(('', port))

    # Set a timeout for receiving the data
    sock.settimeout(time)
    
    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                #print(f"Received response from {addr}: {data}")
                return data , addr
            except socket.timeout:
                return None, None
                break
    finally:
        sock.close()