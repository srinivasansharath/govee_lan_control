# Govee Lan Control Package

This package implements the Govee LED control sequences listed in - https://app-h5.govee.com/user-manual/wlan-guide. Multicast udp packets are used to identify a Govee LED device on the subnet. UDP control packets are used to control its state, color, brightness, etc.

This package has been developed and tested with only one Govee Device on the network i.e. SKU: H6056, https://us.govee.com/products/govee-rgbicww-wifi-bluetooth-flow-plus-light-bars; having multiple Govee devices on the network could cause issues with this package, and this feature will need to be implemented. (maybe once I buy my 2nd Govee device) 

## Installation
```pip install govee_lan_control```

## Usage

```
import time
import random
import govee_lan_device

# Init the device
led = govee_lan_device.GoveLanDevice()

# if device is not found, exit
if led.isInitialized == False:
    exit()

# Print the discovered device
print(f"Discovered Govee LED device: {led.name} at IP: {led.ip} with MAC: {led.mac}")

# Turn on the LED
led.on()

# Set the brightness to 50%
led.brightness(50)

time.sleep(1)

# Set the color to white, and the color temperature to 9000K
led.color([255, 255, 255], 9000)

time.sleep(1)

# Set a random color
led.color(
    [random.randint(0, 255), 
    random.randint(0, 255), 
    random.randint(0, 255)], 
    9600)

time.sleep(1)

# Blink the LED twice
led.blink(2)

# Turn off the LED
led.off()
```