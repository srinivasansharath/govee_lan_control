import udp
import json
import time
from discover import discover_govee_leds

# Govee Multicast Network Parameters
MCAST_GRP = '239.255.255.250'
MCAST_SEND_PORT = 4001
MCAST_RECV_PORT = 4002
DEVICE_CONTROL_PORT = 4003


class GoveLanDevice:
    def __init__(self):
        ip, mac, name = discover_govee_leds()
        if ip == None:
            self.isInitialized = False
        else:
            self.ip = ip
            self.mac = mac
            self.name = name
            self.isInitialized = True
    
    def isInitialized(self):
        return self.isInitialized

    def on(self):
        payload = {
                    "msg":{
                        "cmd":"turn",
                        "data":{
                            "value": 1 # 0 or 1
                        }
                    }
                }
        payload['msg']['data']['value'] = 1
        print("Turning on...")
        udp.send_udp_packet(self.ip, DEVICE_CONTROL_PORT, payload)

    def off(self):
        payload = {
                    "msg":{
                        "cmd":"turn",
                        "data":{
                            "value": 1 # 0 or 1
                        }
                    }
                }
        payload['msg']['data']['value'] = 0
        print("Turning off...")
        udp.send_udp_packet(self.ip, DEVICE_CONTROL_PORT, payload)

    def brightness(self, brightness):
        Bringhtness = int(brightness)
        if brightness > 100:
            brightness = 100
        if brightness < 0:
            brightness = 0
        payload = {
                    "msg":{
                        "cmd":"brightness",
                        "data":{
                            "value": 100 # 0-100
                        }
                    }
                }
        payload['msg']['data']['value'] = Bringhtness
        print(f"Setting brightness to {Bringhtness}%...")
        udp.send_udp_packet(self.ip, DEVICE_CONTROL_PORT, payload)

    def color(self, colors, temp):
        R = int(colors[0])
        G = int(colors[1])
        B = int(colors[2])
        T = int(temp)
        
        # Ensure valid params
        if R > 255:
            R = 225
        elif R < 0: 
            R = 0
        
        if G > 255:
            G = 225
        elif G < 0: 
            G = 0
        
        if B > 255:
            B = 225
        elif B < 0: 
            B = 0
        
        if T > 9000:
            T = 9000
        elif T < 2700:
            T = 2700

        payload = {
                    "msg":{
                        "cmd":"colorwc",
                        "data":{
                            "color": {
                                "r": 255, # 0-255
                                "g": 255, # 0-255
                                "b": 255  # 0-255
                            },
                            "colorTmeInKelvin": 7200 # 2700-9000
                        }
                    }
                }
        payload['msg']['data']['color']['r'] = R
        payload['msg']['data']['color']['g'] = G
        payload['msg']['data']['color']['b'] = B
        payload['msg']['data']['colorTmeInKelvin'] = temp
        print(f"Setting color to {R}, {G}, {B}, {temp}...")
        udp.send_udp_packet(self.ip, DEVICE_CONTROL_PORT, payload)


    def blink(self, reps=1):
        current_state = self.status()
        if not current_state:
            return
        if current_state['onOff'] == 0:
            for i in range(reps):
                self.on()
                time.sleep(1)
                self.off()
                time.sleep(1)
            return
        else:
            for i in range(reps):
                self.off()
                time.sleep(1)
                self.on()
                time.sleep(1)
            return
 
    def status(self):
        payoad = {
                    "msg":{
                        "cmd":"devStatus",
                        "data":{}
                    }
                }
        udp.send_udp_packet(self.ip, DEVICE_CONTROL_PORT, payoad)
        data, addr =  udp.receive_udp_packet(MCAST_GRP, MCAST_RECV_PORT, 5)
        if data:
            print(f"Received message from {addr}: {data}")
            status = json.loads(data.decode('utf-8'))['msg']['data']
            return {
                "onOff": status['onOff'],
                "brightness": status['brightness'],
                "r": status['color']['r'],
                "g": status['color']['g'],
                "b": status['color']['b'],
                "colorTemp": status['colorTemInKelvin']
            }
        else:
            print("No response received")
            return None

