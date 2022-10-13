from machine import Pin
from rp2 import country
from time import sleep
import network
import secrets

led = Pin('LED', Pin.OUT)

def connect(SSID = secrets.SSID, PASSWORD = secrets.PASSWORD):    
    #Wifi init
    print("Starting wifi...")
    country('US') #Region set to avoid issues
    print("Region: US")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) #No powersavings
    print("Powersaving mode: OFF")
    wlan.connect(SSID, PASSWORD) #Network settings from secrets.py
    
    #Connection wait
    max_wait = 10 #10 second connection timeout period
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 0.5 #Half second update interval
        print("waiting for connection to " + SSID + "...")
        sleep(0.5) #Half second update interval

    wlan_status = wlan.status()
    blink_onboard_led(wlan_status)

    #Error handling
    if wlan.status() != 3:
        raise RuntimeError("Network connection failed! Status:", wlan.status())
    else:
        print("\nConnected!")
        status = wlan.ifconfig()
        print("SSID: " + SSID)
        print("IP Addr: " + status[0])
        print("Subnet: " + status[1])
        print("Gateway: " + status[2])
        print("DNS: " + status[3])
        sleep(2)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led.on()
        sleep(.2)
        led.off()
        sleep(.2)