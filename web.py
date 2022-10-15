import network
import ubinascii
import socket
import re
import cpufreq
import ntptime
import picotemp
import urequests as requests
from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)

#Function to load in file to serve   
def get_file(file_name):
    with open(file_name, 'r') as file:
        sfile = file.read()
        file.close()
        
    return sfile

#Listen for connections
def start():
    count = 1
    print("Starting webserver...")
    #HTTP server with socket
    print("Opening socket...")
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Avoids errors for address in use on reconnection
    s.bind(addr)
    s.listen(15)
    print("Listening on:", addr)
    blink_onboard_led(3)
    cpufreq.set(100) #Sets idle CPU frequency

    while True:
        try:
            print("\nWaiting for connection...\n")
            cl, addr = s.accept()
            print("Incoming...")
            led.on()
            cpufreq.set(225) #Increases CPU frequency while serving a request, probably not needed
            
            lan_check = re.search('192.168.1.*', addr[0]) #Checks if the connection is LAN or WAN. WAN clients seem to hold the connection open and hang the server, so a short timeout is needed.
            if lan_check != None: #LAN
                cl.settimeout(5) #Long timeout, just in case.
                print("LAN client connected from:", addr, "ID: {:03d}".format(count))
                
            else: #WAN
                cl.settimeout(1.3) #Short timeout to keep server responsive.
                print("Remote client connected from:", addr, "ID: {:03d}".format(count))
                
            count += 1 #Counter to track how many connections have been made in a session.
            request = cl.recv(1024)
            print("Request received from:", addr[0])
            
            if re.search('Accept: text/html', request): #Checks request for HTML and serves HTML file.
                print("HTML requested from", addr[0])
                rtc = '{:d}:{:02d}:{:02d} {:s}'.format(ntptime.hour(), ntptime.minute(), ntptime.second(), ntptime.hour('local', True)) #Polls RTC for local time and formats it into a usable string.
                date = '{:02d}/{:02d}/{:d}'.format(ntptime.month(), ntptime.day(), ntptime.year()) #Polls RTC for date and formats it into a usable string.
                temp = '{:d}°C | {:d}°F'.format(picotemp.get('c'), picotemp.get('f')) #Polls onboard tempurature sensor and formats it into a usable string.
                response_html = get_file('index.html').format(rtc=rtc, date=date, ip=addr[0], temp=temp) #Loads HTML and inserts generated info.
                cl.send('HTTP/1.1 200 OK\r\nConnection: close\r\nContent-type: text/html\r\n\r\n')
                cl.send(response_html)
                print("HTML sent to:", addr[0])
                
            elif re.search('Accept: text/css', request): #Checks request for CSS and serves CSS file.
                print("CSS requested from", addr[0])
                response_css = get_file('main.css')
                cl.send('HTTP/1.1 200 OK\r\nConnection: close\r\nContent-type: text/css\r\n\r\n')
                cl.send(response_css)
                print("CSS sent to:", addr[0])
                
            elif re.search('Accept: image/', request): #Checks for image and favicon requests, sends a no content reply.
                print("Image requested from", addr[0])
                cl.send('HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n')
                print("'204 No Content' sent to:", addr[0])

            else:
                print("Silly request from:", addr[0], '\n') #Catches all other requests and prints them for curiosity.
                print(request, '\n')
                
            cl.close()
            print("Connection closed: End")
            cpufreq.set(100)
            led.off()
            
        except OSError as e: #Catches timeouts and closes socket.
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
