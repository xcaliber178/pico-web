import cpufreq
import wifi
import webrepl
import ntptime
import web
import _thread

led = machine.Pin("LED", machine.Pin.OUT)
led.off()

cpufreq.set(133)

wifi.connect()
#_thread.start_new_thread(ntptime.settime, ())
#webrepl.start()
ntptime.settime()
web.start()