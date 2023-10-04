from pyPS4Controller.controller import Controller
from rpi_hardware_pwm import HardwarePWM
import time

###################################################
#Intialisation des moteurs
##################################################
#paramètres de la fonction vitesse_m_s, à étalonner
direction_prop = -1# -1 pour les variateurs inversés ou un petit rapport correspond à une marche avant
pwm_stop_prop = 8.10
point_mort_prop = 0.46
delta_pwm_max_prop = 1.5 #pwm à laquelle on atteint la vitesse maximale

vitesse_max_m_s_hard = 8 #vitesse que peut atteindre la voiture
vitesse_max_m_s_soft = 2 #vitesse maximale que l'on souhaite atteindre

direction = -1 #1 pour angle_pwm_min a gauche, -1 pour angle_pwm_min à droite
angle_pwm_min = 6.2   #min
angle_pwm_max = 8.5   #max
angle_pwm_centre= 7.35
angle_degre_max = +18 #vers la gauche
angle_degre=0

pwm_prop = HardwarePWM(pwm_channel=0, hz=50)
pwm_dir = HardwarePWM(pwm_channel=1, hz=50)
print("PWM désactivées")

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
    
def set_vitesse_m_s(vitesse_m_s):
    if vitesse_m_s > vitesse_max_m_s_soft :
        vitesse_m_s = vitesse_max_m_s_soft
    elif vitesse_m_s < -vitesse_max_m_s_hard :
        vitesse_m_s = -vitesse_max_m_s_hard
    if vitesse_m_s == 0 :
        pwm_prop.change_duty_cycle(pwm_stop_prop)
    elif vitesse_m_s > 0 :
        vitesse = vitesse_m_s * (delta_pwm_max_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(pwm_stop_prop + direction_prop*(point_mort_prop + vitesse ))
    elif vitesse_m_s < 0 :
        vitesse = vitesse_m_s * (delta_pwm_max_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(pwm_stop_prop - direction_prop*(point_mort_prop - vitesse ))
        
def recule():
    set_vitesse_m_s(-vitesse_max_m_s_hard)
    time.sleep(0.2)
    set_vitesse_m_s(0)
    time.sleep(0.2)
    set_vitesse_m_s(-1)


a_prop = vitesse_max_m_s_soft/(65198)
a_dir=(angle_degre_max)/(-32767)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def on_R2_press(self,value):
        print("La valeur de R2 est: ",value)
        value += 32767
        set_vitesse_m_s(a_prop*value)
        
    def on_R2_release(self):
         #print("Arrêt complet")
         set_vitesse_m_s(0)
 
    def on_L3_x_at_rest(self):
        set_direction_degre(0)
        
    def on_R1_press(self):
        recule()
        
    def on_R1_release(self):
        set_vitesse_m_s(0)
    
    def on_L3_right(self,value):
        set_direction_degre(a_dir*value)

    def on_L3_left(self,value):
        set_direction_degre(a_dir*value)
        
    def on_L2_press(self, value):
        set_vitesse_m_s(-vitesse_max_m_s_hard)
        
    def on_L2_release(self):
        set_vitesse_m_s(0)
        
    def on_x_press(self):
        pwm_prop.stop()
        pwm_dir.stop()
        print("PWM désactivées")
        
    def on_circle_press(self):
        pwm_prop.start(pwm_stop_prop)
        pwm_dir.start(angle_pwm_centre)
        print("PWM activées")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()


