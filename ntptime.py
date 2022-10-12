import time as utime
import socket
import struct
import _thread
from machine import Pin, RTC

led = Pin("LED", Pin.OUT)

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"

def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    
    ntp_recv = False
    error = False
    fatal = False
    ntp_try = 0
    while ntp_recv is False:
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            if ntp_try == 10:
                from sys import exit
                raise Exception("ExcessiveAttempts") 
            elif error:
                print("Retrying...(", ntp_try, "/10)", sep='')
                utime.sleep(1)
                s.settimeout(2)
            else:
                s.settimeout(2)
                print("Connecting to NTP server...")
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        except OSError as e:
            print("Error: ", e)
            error = True
        except Exception as e:
            print("Fatal Error:", e)
            print("Exiting!")
            fatal = True
        else:
            ntp_recv = True
            error = False
        finally:
            s.close()
            ntp_try += 1
            if fatal:
                for i in range(40):
                    led.on()
                    utime.sleep(.07)
                    led.off()
                    utime.sleep(.07)
                
    val = struct.unpack("!I", msg[40:44])[0]

    EPOCH_YEAR = utime.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600
    elif EPOCH_YEAR == 1970:
        # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 2208988800
    else:
        raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def settime():
    print("Starting NTP sync...")
    t = time()

    tm = utime.gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
    print("Time synced to " + host)
    print(tm[3], ":", tm[4], ":", tm[5], " UTC", sep='')
    
def currenttime(req = 'c'):
    if req is 'c':
        currenttime = RTC().datetime()[4]-5, RTC().datetime()[5], RTC().datetime()[6]
        return currenttime
    elif req is 'h':
        hour = RTC().datetime()[4]-5
        return hour
    elif req is 'm':
        minute = RTC().datetime()[5]
        return minute
    elif req is 's':
        second = RTC().datetime()[6]
        return second
def currentdate(req = 'c'):
    if req is 'c':
        currentdate = RTC().datetime()[1], RTC().datetime()[2], RTC().datetime()[3]
        return currentdate