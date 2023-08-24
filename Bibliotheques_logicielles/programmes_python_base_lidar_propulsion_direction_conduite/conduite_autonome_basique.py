from rplidar import RPLidar
import numpy as np
import time
from rpi_hardware_pwm import HardwarePWM

#paramètres fonction vitesse_m_s, étalonnés avec test_pwm_propulsion.py
stop_prop = 7.5
point_mort_prop = 0.5
pwm_max = 9 #pwm à laquelle on atteint la vitesse maximale

vitesse_max_m_s_hard = 8 #vitesse que peut atteindre la voiture
vitesse_max_m_s_soft = 2 #vitesse maximale que l'on souhaite atteindre

#paramètres fonction set_direction_m_s, étalonnés via test_pwm_direction.py
direction = 1 #1 pour angle_pwm_min a gauche, -1 sinon
angle_pwm_min = 6.2   #min
angle_pwm_max = 8.7   #max
angle_pwm_centre= 7.4

angle_degre_max = +18 #vers la gauche
angle_degre=0

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
    
#connexion et démarrage du lidar
lidar = RPLidar("/dev/ttyUSB0",baudrate=115200)
lidar.connect()
print (lidar.get_info())
lidar.start_motor()
time.sleep(1)

tableau_lidar_mm = [0]*360 #création d'un tableau de 360 zéros


try : 
    for scan in lidar.iter_scans(scan_type='express') : 
    #Le tableau se remplissant continuement, la boucle est infinie
        #rangement des données dans le tableau
        for i in range(len(scan)) :
            angle = min(359,max(0,359-int(scan[i][1]))) #scan[i][1] : angle 
            tableau_lidar_mm[angle]=scan[i][2]  #scan[i][2] : distance    
        #############################################
        ## Code de conduite (issu du simulateur ou non)
        #############################################
            
        #l'angle de la direction est la différence entre les mesures  
        #des rayons du lidar à -60 et +60°  
        angle_degre = 0.02*(tableau_lidar_mm[60]-tableau_lidar_mm[-60])
        set_direction_degre(angle_degre)
        vitesse_m_s = 0.5
        set_vitesse_m_s(vitesse_m_s)    
        ##############################################
except KeyboardInterrupt: #récupération du CTRL+C
    print("fin des acquisitions")

#arrêt et déconnexion du lidar et des moteurs
lidar.stop_motor()
lidar.stop()
time.sleep(1)
lidar.disconnect()
pwm_dir.stop()
pwm_prop.stop()


