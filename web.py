from machine import Pin
from time import sleep
import urequests as requests
import network
import ubinascii
import socket
import re
import cpufreq
import ntptime

led = Pin("LED", Pin.OUT)

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# Listen for connections
def start():
    print("Starting webserver...")
    #HTTP server with socket
    print("\n")
    print("Opening socket...")
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoids errors for address in use on reconnection
    s.bind(addr)
    s.listen(15)
    print('Listening on:', addr)
    blink_onboard_led(3)
    
    count = 0
    while True:
        try:
            print("\nWaiting for connection...")
            cl, addr = s.accept()
            cpufreq.set(200, False)
            led.on()
            
            lan_check = re.search('192.168.1.*', addr[0])
            if lan_check != None:
                cl.settimeout(None)
                print('\nLAN client connected from:', addr, count)
            else:
                cl.settimeout(1.3)
                print('\nRemote client connected from:', addr, count)
                
            cpufreq.get()
            count += 1
            request = cl.recv(1024)
            print("Request received from:", addr[0])
            
            rtc = "{:02d}:{:02d}:{:02d}".format(ntptime.currenttime()[0], ntptime.currenttime()[1], ntptime.currenttime()[2])
            date = "{:02d}/{:02d}/{:d}".format(ntptime.currentdate()[0], ntptime.currentdate()[1], ntptime.currentdate()[2])
            response = get_html('index.html') % (rtc, date)
            cl.send("HTTP/1.0 200 OK\r\nConnection: close\r\nContent-type: text/html\r\n\r\n")
            cl.send(response)
            print("Response sent to:", addr[0])
            
            cl.close()
            print('Connection closed: End')
            cpufreq.set(125)
            led.off()
            
        except OSError as e:
            cl.close()
            print('Connection closed: Timeout')
            cpufreq.set(125)
            led.off()

def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led.on()
        sleep(.1)
        led.off()
        sleep(.1)