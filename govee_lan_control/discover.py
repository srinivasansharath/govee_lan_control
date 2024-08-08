import udp
import json

# Govee Multicast Network Parameters
MCAST_GRP = '239.255.255.250'
MCAST_SEND_PORT = 4001
MCAST_RECV_PORT = 4002

# Govee Multicast UDP Packet
discover_message = {
    "msg":{
        "cmd":"scan",
        "data":{
            "account_topic":"reserve"
        }
    }
}

# Discover Govee LED devices on the local network
def discover_govee_leds():
    udp.send_udp_packet(MCAST_GRP, MCAST_SEND_PORT, discover_message)
    data, addr =  udp.receive_udp_packet(MCAST_GRP, MCAST_RECV_PORT, 5)
    if data == None:
        print("No Govee LED devices found on the network.")
        return None, None, None
    else:
        print(f"Received message from {addr}: {data}")
        discovery_data = json.loads(data.decode('utf-8'))
        #TODO: In case of multiple Govee devices on the network, return a list of IPs    
        ip = discovery_data['msg']['data']['ip']
        mac = discovery_data['msg']['data']['device']
        name = discovery_data['msg']['data']['sku']
        return ip, mac, name

if __name__ == "__main__":
    ip = discover_govee_leds()
    print(f"Govee LED device discovered at: {ip}")