from gpiozero import LED, Button
from signal import pause
import time

bp1 = Button("GPIO5")
bp2 = Button("GPIO6")
led1 = LED("GPIO17")
led2 = LED("GPIO27")

bp1.when_pressed = led1.on
bp1.when_released = led1.off

led1.on()
time.sleep(2)
led1.off()

while True :
    if bp2.is_pressed:
        print("Bouton2 enfoncé")
    else:
        print("Bouton2 relâché")