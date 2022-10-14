import network
import ubinascii
import socket
import re
import cpufreq
import ntptime
import urequests as requests
from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)

# Function to load in html page    
def get_file(file_name):
    with open(file_name, 'r') as file:
        sfile = file.read()
        file.close()
        
    return sfile

# Listen for connections
def start():
    count = 1
    print("Starting webserver...")
    #HTTP server with socket
    print("Opening socket...")
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoids errors for address in use on reconnection
    s.bind(addr)
    s.listen(15)
    print("Listening on:", addr)
    blink_onboard_led(3)
    cpufreq.set(100)

    while True:
        try:
            print("\nWaiting for connection...\n")
            cl, addr = s.accept()
            print("Incoming...")
            led.on()
            cpufreq.set(225)
            
            lan_check = re.search('192.168.1.*', addr[0])
            if lan_check != None:
                cl.settimeout(5) #Just in case client hangs.
                print("LAN client connected from:", addr, "ID: {:03d}".format(count))
                
            else:
                cl.settimeout(1.3)
                print("Remote client connected from:", addr, "ID: {:03d}".format(count))
                
            count += 1
            request = cl.recv(1024)
            print("Request received from:", addr[0])
            
            if re.search('Accept: text/html', request):
                print("HTML requested from", addr[0])
                rtc = '{:d}:{:02d}:{:02d} {:s}'.format(ntptime.hour(), ntptime.minute(), ntptime.second(), ntptime.hour('local', True))
                date = '{:02d}/{:02d}/{:d}'.format(ntptime.month(), ntptime.day(), ntptime.year())
                response_html = get_file('index.html').format(rtc=rtc, date=date)
                cl.send('HTTP/1.1 200 OK\r\nConnection: close\r\nContent-type: text/html\r\n\r\n')
                cl.send(response_html)
                print("HTML sent to:", addr[0])
                
            elif re.search('Accept: text/css', request):
                print("CSS requested from", addr[0])
                response_css = get_file('main.css')
                cl.send('HTTP/1.1 200 OK\r\nConnection: close\r\nContent-type: text/css\r\n\r\n')
                cl.send(response_css)
                print("CSS sent to:", addr[0])
                
            elif re.search('Accept: image/', request):
                print("Image requested from", addr[0])
                cl.send('HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n')
                print("'204 No Content' sent to:", addr[0])
            else:
                print("Silly request from:", addr[0], '\n')
                print(request, '\n')
            cl.close()
            print("Connection closed: End")
            cpufreq.set(100)
            led.off()
            
        except OSError as e:
            cl.close()
            print("Connection closed: Timeout")
            cpufreq.set(100)
            led.off()

def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led.on()
        sleep(.1)
        led.off()
        sleep(.1)
