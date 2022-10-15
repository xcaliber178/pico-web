import socket
import struct
import time as utime
from machine import Pin
from machine import RTC

led = Pin('LED', Pin.OUT)

host = 'pool.ntp.org'

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
            led.on()
            if ntp_try == 10:
                from sys import exit
                raise Exception('ExcessiveAttempts')

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
            print("Error:", e)
            error = True

        except Exception as e:
            print("Fatal Error:", e)
            print("Exiting!")
            fatal = True

        else:
            ntp_recv = True
            error = False
            led.off()

        finally:
            s.close()
            ntp_try += 1
            led.off()
            if fatal:
                for i in range(40):
                    led.on()
                    utime.sleep(.07)
                    led.off()
                    utime.sleep(.07)
                led.on()
                
    val = struct.unpack('!I', msg[40:44])[0]

    EPOCH_YEAR = utime.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600

    elif EPOCH_YEAR == 1970:
        # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 2208988800

    else:
        raise Exception('Unsupported epoch: {}'.format(EPOCH_YEAR))

    return val - NTP_DELTA


#RTC is set in UTC time.
def settime():
    print("Starting NTP sync...")
    t = time()
    tm = utime.gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
    print("Time synced to " + host)
    print('{:d}:{:02d}:{:02d}'.format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6]))
    
def second():
    return RTC().datetime()[6]

def minute():
    return RTC().datetime()[5]

def hour(tz = 'local', m = False):
    utc = RTC().datetime()[4]
    if tz is 'local' and m is False:
        if utc == 5:
            local = 12
        elif utc < 5:
            local = utc+7
        elif utc > 17:
            local = utc-17
        else:
            local = utc-5
        return local
    
    if tz is 'local' and m is True:
        if utc > 17 or utc <= 5:
            return 'pm'
        else:
            return 'am'
    else:
        return utc
    
def day():
    return RTC().datetime()[2]

def month():
    return RTC().datetime()[1]

def year():
    return RTC().datetime()[0]