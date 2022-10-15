from machine import ADC

sensor = ADC(4)
conversion = 3.3/(65535)

def get(unit = 'c'):
    sensor_raw = sensor.read_u16() * conversion
    tempC = 27 - (sensor_raw - 0.706)/0.001721
    tempF = (27 - (sensor_raw - 0.706)/0.001721) * 9 / 5 + 32
    #print(tempF,"*F", "   ", tempC,"*C")
    if unit is 'c' or unit is 'C':
        return int(tempC)
    elif unit is 'f' or unit is 'F':
        return int(tempF)
    else:
        print("Error: Invalid tempurature request!")
        return 'Error!'