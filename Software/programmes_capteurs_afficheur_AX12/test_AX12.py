import time
import serial
import numpy as np

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

def set_direction_degre(angle_degre) :
    cmd = 512 - 43 - int(angle_degre * 2.2)
    if cmd > 542 :
        cmd = 542
    if cmd < 397 :
        cmd = 397
    cmd_LSB = cmd & 0xFF
    cmd_MSB = (cmd & 0xFF00)>>8
    checksum = (~(39 + cmd_LSB + cmd_MSB))&0xff
    frame = bytearray(9)    
    frame[0] = np.uint8(255)
    frame[1] = np.uint8(255)
    frame[2] = np.uint8(1)
    frame[3] = np.uint8(5)
    frame[4] = np.uint8(3)
    frame[5] = np.uint8(30)
    frame[6] = np.uint8(cmd_LSB) #poids faible
    frame[7] = np.uint8(cmd_MSB) #poids fort
    frame[8] = np.uint8(checksum)
    port.write(frame)
    
# passage en 115200 bit/s
# port.write(bytearray.fromhex("FF FF 01 04 03 04 10 E3"))

while True:
        set_direction_degre(0)
        time.sleep(1)
        set_direction_degre(-30) #droite
        time.sleep(2)
        set_direction_degre(0)
        time.sleep(1)
        set_direction_degre(30) #gauche
        time.sleep(2)
        
        