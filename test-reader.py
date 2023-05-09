import usb.core 
import usb.util 
import time
import RPi.GPIO as GPIO

USB_IF      = 0 # Interface 
USB_TIMEOUT = 5 # Timeout in MS 
USB_VENDOR  = 0xffff # Vendor-ID:  
USB_PRODUCT = 0x0035 # Product-ID 

# Find the HID device by vender/product ID
dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT) 

# Get and store the endpoint 
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True: 
    try:
        dev.detach_kernel_driver(USB_IF)
    except:
        sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(USB_IF, str(e)))

# Claim the device 
usb.util.claim_interface(dev, USB_IF) 

# Configure the Raspberry Pi GPIO
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11, GPIO.OUT) 

receivedNumber = 0 
control = None

# Read input
while True:
    try: 
        # Read a character from the device
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        print(control)
    except KeyboardInterrupt: 
        GPIO.cleanup() 
    except Exception as e: 
        pass

    time.sleep(.01) # Let CTRL+C actually exit