from rplidar import RPLidar
import numpy as np
import time
from rpi_hardware_pwm import HardwarePWM
import threading

#paramètres de la fonction vitesse_m_s
direction_prop = -1 # -1 pour les variateurs inversés ou un petit rapport correspond à une marche avant
pwm_stop_prop = 8.17
point_mort_prop = 0.13
delta_pwm_max_prop = 1.5 #pwm à laquelle on atteint la vitesse maximale

vitesse_max_m_s_hard = 8 #vitesse que peut atteindre la voiture
vitesse_max_m_s_soft = 2 #vitesse maximale que l'on souhaite atteindre

#paramètres de la fonction set_direction_degre
direction = 1 #1 pour angle_pwm_min a gauche, -1 pour angle_pwm_min à droite
angle_pwm_min = 6   #min
angle_pwm_max = 9   #max
angle_pwm_centre= 7.5

angle_degre_max = +18 #vers la gauche
angle_degre=0

pwm_prop = HardwarePWM(pwm_channel=0, hz=50)
pwm_prop.start(pwm_stop_prop)

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

acqui_tableau_lidar_mm = [0]*360 #création d'un tableau de 360 zéros
tableau_lidar_mm = [0]*360
drapeau_nouveau_scan = False
Run_Lidar = False

def lidar_scan() :
    global drapeau_nouveau_scan
    global acqui_tableau_lidar_mm
    global Run_Lidar
    global lidar
    print ("tâche lidar_scan démarrée")
    while Run_Lidar == True :
        try : 
            for scan in lidar.iter_scans(scan_type='express') : 
            #Le tableau se remplissant continuement, la boucle est infinie
                #rangement des données dans le tableau
                for i in range(len(scan)) :
                    angle = min(359,max(0,359-int(scan[i][1]))) #scan[i][1]:angle 
                    acqui_tableau_lidar_mm[angle]=scan[i][2]    #scan[i][2]:distance
                drapeau_nouveau_scan = True
                time.sleep(0.01)
                if(Run_Lidar == False) :
                    break
        except :
            print("souci acquisition lidar")

def conduite_autonome():
    global drapeau_nouveau_scan
    global acqui_tableau_lidar_mm
    global tableau_lidar_mm
    global Run_Lidar
    print ("tâche conduite autonome démarrée")
    while Run_Lidar == True :
        if(drapeau_nouveau_scan == False) :
            time.sleep(0.01)
        else :
            #récupération du tableau_lidar acquis par l'autre thread
            for i in range(-100,101) :
                tableau_lidar_mm[i] = acqui_tableau_lidar_mm[i]        
            drapeau_nouveau_scan = False
            
            ####################################################
            # programme de conduite avec détection des murs et marche arrière
            ###################################################
            
            if tableau_lidar_mm[0]>0 and tableau_lidar_mm[0]<150:
                print("mur devant")
                set_direction_degre(0)
                recule()
                time.sleep(0.5)
            

            elif tableau_lidar_mm[-30]>0 and tableau_lidar_mm[-30]<150 :
                print("mur à droite")
                set_direction_degre(-18)
                recule()
                time.sleep(0.5)
            
            elif tableau_lidar_mm[30]>0 and tableau_lidar_mm[30]<150 :
                print("mur à gauche")
                set_direction_degre(+18)
                recule()
                time.sleep(0.5)
            
            else :
                #l'angle de la direction est la différence entre les mesures des rayons 
                #du lidar à -60 et +60°
                angle_degre = 0.02*(tableau_lidar_mm[60]-tableau_lidar_mm[-60])
                set_direction_degre(angle_degre)
                vitesse_m_s = 0.5
                set_vitesse_m_s(vitesse_m_s)
                            
            ###################################################

         
#connexion et démarrage du lidar
lidar = RPLidar("/dev/ttyUSB0",baudrate=115200)
lidar.connect()
print (lidar.get_info())
lidar.start_motor()
time.sleep(2)

#démarrage des 2 thread
Run_Lidar = True
thread_scan_lidar = threading.Thread(target= lidar_scan)
thread_scan_lidar.start()
time.sleep(1)
thread_conduite_autonome = threading.Thread(target = conduite_autonome)
thread_conduite_autonome.start()

while True :
    try : 
        pass
    except KeyboardInterrupt: #récupération du CTRL+C
        print("arrêt du programme")
        Run_Lidar = False
        break

#attente de l'arrêt des tâches    
thread_conduite_autonome.join()
thread_scan_lidar.join()          

#arrêt et déconnexion du lidar
lidar.stop_motor()
lidar.stop()
time.sleep(1)
lidar.disconnect()
pwm_prop.stop()
pwm_dir.stop()

   

        












