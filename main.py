import cpufreq
import wifi
#import webrepl
import ntptime
import web
from machine import Pin

led = Pin('LED', Pin.OUT)
led.off() #Makes sure the LED isn't left on during a reset

cpufreq.set(150) #Sets the initial CPU frequency to 150MHz (default is 125MHz, stock max is 133MHz) to ensure a speedy start up.
print('')
wifi.connect() #Starts wifi connection process
print('')
#webrepl.start()
ntptime.settime() #Starts NTP sync process
print('')
web.start() #Starts webserver and blocks