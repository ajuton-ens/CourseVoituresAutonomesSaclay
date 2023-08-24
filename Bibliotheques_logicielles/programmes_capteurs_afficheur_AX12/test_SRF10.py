import smbus
import time
bus = smbus.SMBus(1)
address = 0x70

#REQUIRES 5V
def write(value):
        bus.write_byte_data(address, 0, value)
        return -1

def range():
        MSB = bus.read_byte_data(address, 2)
        LSB = bus.read_byte_data(address, 3)
        range = (MSB << 8) + LSB
        return range
    
while True:
        write(0x51)
        time.sleep(0.7)
        rng = range()
        print (rng)
