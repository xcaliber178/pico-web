import cpufreq
import wifi
import webrepl
import ntptime
import web
from machine import Pin

led = Pin('LED', Pin.OUT)
led.off()

cpufreq.set(150)
print('')
wifi.connect()
print('')
#webrepl.start()
ntptime.settime()
print('')
web.start()