import usb.core 
import usb.util 
import time
import json
import RPi.GPIO as GPIO

import spotipy
from spotipy.oauth2 import SpotifyOAuth


data = json.load(open('data.json', 'r', encoding='utf-8'))


def main():
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

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=data["spotify"]["client_id"],
        client_secret=data["spotify"]["client_secret"],
        redirect_uri="http://localhost",
        scope="user-modify-playback-state",
        open_browser=False,
        cache_path='./tokens.txt'
    ))

    input_str = ""
    while True:
        try: 
            # Read a character from the device 
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            input_substr = get_input_char(control) 
            input_str += input_substr
            if len(input_str) == 22:
                print("Input: " + input_str)
                album_id = get_album_id(input_str)
                if album_id:
                    print("Album ID: " + album_id)
                    
                    # Play album using Spotify API
                    sp.start_playback(context_uri='spotify:album:' + album_id, device_id=data["spotify"]["device_id"])
                input_str = ""
        except KeyboardInterrupt: 
            GPIO.cleanup() 
        except Exception as e: 
            pass

        time.sleep(.01) # Let CTRL+C actually exit


def get_input_char(input):
    for n in input:
        if n != 0:
            return str(n).zfill(2)
    return ""


def get_album_id(input_str):
    # Fetch the corresponding album ID based on the RFID tag
    for album in data["spotify"]["albums"]:
        if sorted(album["rfid"]) == sorted(input_str):
            print("Album: " + album["title"])
            return album["album_id"]

main()
