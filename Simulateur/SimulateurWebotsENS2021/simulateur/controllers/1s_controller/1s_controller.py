import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import cmath as cm
import time
#from iterative_closest_point import icp_matching
#import field
from scipy.signal import butter, filtfilt

BALISE=[
        [[0,5],[0,2]],
        [[-2,5],[-2,3]],
        [[-4,4],[-1,2]],
        [[-4,2],[-2,2]],
        [[-2,0],[1,0]],
        [[1,-3],[-1,-3]],
        [[-5,-3],[-1,-3]],
        [[-2,-5],[-2,-3]],
        [[0,-5],[0,-2.5]],
        [[2,-5],[2,-2]],
        [[2,-2],[5,-2]],
        [[2,0],[5,0]],
        [[1.5,2],[5,2]],
        [[1.5,2],[2,5]],
]

Verbose_race=False

if Verbose_race:
    plt.style.use('fivethirtyeight')
    Race_fig=plt.figure()
    ax_race = Race_fig.add_subplot(1, 1, 1)
    img = plt.imread("circuit2.png")
    ax_race.imshow(img, extent=[-5, 5, 5, -5])

from vehicle import Driver
driver = Driver()

basicTimeStep = int(driver.getBasicTimeStep())
sensorTimeStep = 4 *basicTimeStep

from controller import Field
robot_node = driver.getFromDef("Car")
trans_field = robot_node.getField("translation")
rot_field = robot_node.getField("rotation")


from controller import Lidar
from lidar import GetLidarDatas
lidar = Lidar("lidar")
lidar.enable(4*basicTimeStep)
lidar.enablePointCloud()
lidar_number_points=lidar.getNumberOfPoints()
angle_resolution=(2*np.pi)/lidar_number_points
L1=list(range(int(lidar_number_points/4)))
L2=list(range(int(lidar_number_points*3/4),lidar_number_points))
L1.reverse()
L2.reverse()
L2.pop()
L=L1+L2
print(L)


from controller import Camera
from pixy import GetPixyDatas2 as GetPixyDatas
camera = Camera("camera")
cam_width=camera.getWidth()
cam_height=camera.getHeight()
camera.enable(basicTimeStep)


from controller import TouchSensor
from SimulationState import SimulationState
ts1=TouchSensor("touch sensor 1")
ts2=TouchSensor("touch sensor 2")
ts3=TouchSensor("touch sensor 3")
ts4=TouchSensor("touch sensor 4")
ts5=TouchSensor("touch sensor 5")
ts6=TouchSensor("touch sensor 6")
ts1.enable(basicTimeStep)
ts2.enable(basicTimeStep)
ts3.enable(basicTimeStep)
ts4.enable(basicTimeStep)
ts5.enable(basicTimeStep)
ts6.enable(basicTimeStep)
TS=[ts1,ts2,ts3,ts4,ts5,ts6]

from Strat_traj import trajectoire1,Demi_tour_narvallo,trajectoire2
from ransac import ransac_polyfit
from DetectionObstacle import ObstacleDetection,ObstacleAndWallDetectionDebug,ClusteringLidarCloud,AvoidObstacle


Sens_course=True
angle = 0
vitesse = 0
Marche = False

VirageDroiteSerre=False
VirageGaucheSerre=False

it=0

while driver.step() != -1:
    if it<10:
        it=it+1
    
    Green_wall,Red_wall=GetPixyDatas(camera,cam_width,cam_height,Verbose=False)
    #print(Green_wall,Red_wall)

    if Green_wall[0][0] != None and Red_wall[0][0] != None :
        #print("Bg :",Green_wall[0][1])
        #print("Br :",Red_wall[0][1])
        Bg = Green_wall[0][1]
        Br = Red_wall[0][1]
        if Bg-Br > 0:
            Sens_course = True
        else :
            Sens_course = False

    ObstacleList=[]
    lidar_datas=GetLidarDatas(lidar,lidar_number_points)
    if it==10:
        if Sens_course :
            angle,vitesse,VirageDroiteSerre,VirageGaucheSerre=trajectoire2(lidar_datas,lidar_number_points,VirageDroiteSerre,VirageGaucheSerre)
            Marche=False
        else :
            angle,vitesse,Marche=Demi_tour_narvallo(lidar_datas,lidar_number_points,Marche)

    driver.setCruisingSpeed(5)
    driver.setSteeringAngle(angle)
    ObstacleAndWallDetectionDebug(lidar_datas,lidar_number_points,L)
    State=SimulationState(driver,robot_node,trans_field,rot_field,TS)
    
    

