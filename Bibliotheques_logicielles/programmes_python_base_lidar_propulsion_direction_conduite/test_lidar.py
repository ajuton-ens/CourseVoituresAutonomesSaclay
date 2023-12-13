from rplidar import RPLidar
import numpy as np
import time
import matplotlib.pyplot as plt

#connexion et démarrage du lidar
lidar = RPLidar("/dev/ttyUSB0",baudrate=256000)
lidar.connect()
print (lidar.get_info())
lidar.start_motor()
time.sleep(1)

tableau_lidar_mm = [0]*360 #création d'un tableau de 360 zéros

try : 
    for scan in lidar.iter_scans(scan_type='express') : 
    #Le tableau se remplissant continuement, la boucle est infinie
        #affichage du nombre de points récupérés lors du tour, pour les tests
        print("nb pts : " + str(len(scan))) 
        #rangement des données dans le tableau
        for i in range(len(scan)) :
            angle = min(359,max(0,359-int(scan[i][1]))) #scan[i][1] : angle 
            tableau_lidar_mm[angle]=scan[i][2]          #scan[i][2] : distance       

except KeyboardInterrupt: #récupération du CTRL+C
    print("fin des acquisitions")

#arrêt et déconnexion du lidar
lidar.stop_motor()
lidar.stop()
time.sleep(1)
lidar.disconnect()

#affichage des données acquises sur l'environnement

teta = [0]*360 #création d'un tableau de 360 zéros

for i in range(360) :
    teta[i]=i*np.pi/180

fig = plt.figure()
ax = plt.subplot(111, projection='polar')
line = ax.scatter(teta, tableau_lidar_mm, s=5)
line.set_array(tableau_lidar_mm)
ax.set_rmax(8000)
ax.grid(True)
plt.show()
