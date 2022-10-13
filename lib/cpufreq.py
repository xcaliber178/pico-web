from machine import freq

def set(frq = 125, show = True):
    freq(frq * 1000000)
    if show == True:
        print("CPU Frequency: ", frq, "MHz", sep='')
        
def get():
    print("CPU Frequency: ", freq()/1000000, "MHz", sep='')