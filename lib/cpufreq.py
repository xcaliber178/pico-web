from machine import freq

def set(frq = 125, show = True):
    freq(frq * 1000000)
    if show == True:
        print("CPU Frequency: ", frq, "MHz\n", sep='')
        
def get():
    print(freq() / 1000000)