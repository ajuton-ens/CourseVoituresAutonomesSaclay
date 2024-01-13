from rpi_hardware_pwm import HardwarePWM
import time

#paramètres de départ, avec des butées très proche du centre
direction = -1 #1 pour angle_pwm_min a gauche, -1 pour angle_pwm_min à droite
angle_pwm_min = 6.6   #min
angle_pwm_max = 8.9   #max
angle_pwm_centre= 7.75

angle_degre_max = +18 #vers la gauche
angle_degre=0

pwm_dir = HardwarePWM(pwm_channel=1,hz=50)
pwm_dir.start(angle_pwm_centre)

def set_direction_degre(angle_degre) :
    global angle_pwm_min
    global angle_pwm_max
    global angle_pwm_centre
    angle_pwm = angle_pwm_centre + direction * (angle_pwm_max - angle_pwm_min) * angle_degre /(2 * angle_degre_max )
    if angle_pwm > angle_pwm_max : 
        angle_pwm = angle_pwm_max
    if angle_pwm < angle_pwm_min :
        angle_pwm = angle_pwm_min
    pwm_dir.change_duty_cycle(angle_pwm)

print("réglage des butées, Q pour quitter")
print("valeur numérique pour tester un angle de direction")
print("I pour inverser droite et gauche")
print("g pour diminuer la butée gauche et G pour l'augmenter")
print("d pour diminuer la butée droite et D pour l'augmenter")

while True :
    a = input("angle, I, g, G, d, D ?")
    try :
        angle_degre=int(a)
        set_direction_degre(angle_degre)
    except :        
        if a == "I" :
            direction = -direction
            print("nouvelle direction : " + str(direction))
        elif a == "g" :
            if direction == 1 :
                angle_pwm_max -=0.1
                print("nouvelle butée gauche : " + str(angle_pwm_max))
            else :
                angle_pwm_min +=0.1
                print("nouvelle butée gauche : " + str(angle_pwm_min))
            angle_pwm_centre = (angle_pwm_max+angle_pwm_min)/2
            set_direction_degre(18)
        elif a == "G" :
            if direction == 1 :
                angle_pwm_max +=0.1
                print("nouvelle butée gauche : " + str(angle_pwm_max))
            else :
                angle_pwm_min -=0.1
                print("nouvelle butée gauche : " + str(angle_pwm_min))
            angle_pwm_centre = (angle_pwm_max+angle_pwm_min)/2
            set_direction_degre(18)
        elif a == "d" :
            if direction == -1 :
                angle_pwm_max -=0.1
                print("nouvelle butée droite : " + str(angle_pwm_max))
            else :
                angle_pwm_min +=0.1
                print("nouvelle butée droite : " + str(angle_pwm_min))
            angle_pwm_centre = (angle_pwm_max+angle_pwm_min)/2
            set_direction_degre(-18)
        elif a == "D" :
            if direction == -1 :
                angle_pwm_max +=0.1
                print("nouvelle butée droite : " + str(angle_pwm_max))
            else :
                angle_pwm_min -=0.1
                print("nouvelle butée droite : " + str(angle_pwm_min))
            angle_pwm_centre = (angle_pwm_max+angle_pwm_min)/2
            set_direction_degre(-18)
        else :
            break

print("nouvelles valeurs")
print("direction : "        + str(direction))
print("angle_pwm_min : "    + str(angle_pwm_min))
print("angle_pwm_max : "    + str(angle_pwm_max))
print("angle_pwm_centre : " + str(angle_pwm_centre))