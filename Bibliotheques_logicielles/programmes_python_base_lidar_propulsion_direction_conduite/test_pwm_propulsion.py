from rpi_hardware_pwm import HardwarePWM
import time

#paramètres de la fonction vitesse_m_s, à étalonner
stop_prop = 7.5
point_mort_prop = 0.5
pwm_max = 9 #pwm à laquelle on atteint la vitesse maximale

vitesse_max_m_s_hard = 8 #vitesse que peut atteindre la voiture
vitesse_max_m_s_soft = 2 #vitesse maximale que l'on souhaite atteindre

pwm_prop = HardwarePWM(pwm_channel=0, hz=50)
pwm_prop.start(stop_prop)

def set_vitesse_m_s(vitesse_m_s):
    if vitesse_m_s > vitesse_max_m_s_soft :
        vitesse_m_s = vitesse_max_m_s_soft
    elif vitesse_m_s < -vitesse_max_m_s_hard :
        vitesse_m_s = -vitesse_max_m_s_hard
    if vitesse_m_s == 0 :
        pwm_prop.change_duty_cycle(stop_prop)
    elif vitesse_m_s > 0 :
        vitesse = vitesse_m_s * (pwm_max-stop_prop-point_mort_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(stop_prop + point_mort_prop + vitesse )
    elif vitesse_m_s < 0 :
        vitesse = vitesse_m_s * (pwm_max-stop_prop-point_mort_prop)/vitesse_max_m_s_hard
        pwm_prop.change_duty_cycle(stop_prop - point_mort_prop + vitesse )
        
def recule():
    set_vitesse_m_s(-vitesse_max_m_s_hard)
    time.sleep(0.2)
    set_vitesse_m_s(0)
    time.sleep(0.1)
    set_vitesse_m_s(-1)
    
set_vitesse_m_s(0)
time.sleep(1)
set_vitesse_m_s(1.0)
time.sleep(1)
recule()
time.sleep(1)
set_vitesse_m_s(1.0)
time.sleep(1)
set_vitesse_m_s(0)
