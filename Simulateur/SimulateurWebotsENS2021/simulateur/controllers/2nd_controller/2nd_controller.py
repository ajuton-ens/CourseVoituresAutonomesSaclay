import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import cmath as cm
import time
import cv2
#from iterative_closest_point import icp_matching
#import field
from scipy.signal import butter, filtfilt
from matplotlib import pyplot as plt


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

from Strat_traj import trajectoire1,Demi_tour_narvallo


#from rectangle_fitting import LShapeFitting
#from simulator import LidarSimulator

#l_shape_fitting = LShapeFitting()
#lidar_sim = LidarSimulator()

Sens_course=True
angle = 0
vitesse = 0
Marche = False

while driver.step() != -1:

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


    lidar_datas=GetLidarDatas(lidar,lidar_number_points)
    x = []
    y = []

    dist_lid = lidar_datas[:,0]/15
    angle_lid=np.deg2rad(lidar_datas[:,1])

    x = dist_lid*np.sin(angle_lid)  ###WARNING
    y = dist_lid*np.cos(angle_lid)

    x[x>512] = 0
    y[y>512] = 0

    # plt.clf()
    # plt.plot(x,y,'*')
    # plt.show()
    # plt.pause(.1)
    # time.sleep(0.01)

    data = np.zeros( (1024,1024,1), dtype=np.uint8)
    for i in range(len(x)):
        data[512+round(y[i]),512+round(x[i])] = 255

    lines = cv2.HoughLinesP(data, 1, np.pi/180, 20, minLineLength=1, maxLineGap=30)
        # Draw lines on the image

    lines2 = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        coef = (y2-y1)+(x2-x1)
        lines2.append([x1,y1,x2,y2,coef])
    line3 = []
    print("Damned")
    print(lines2)
    while lines2:
        print(lines2)
        print(line3)
        print("OP")
        x1_1,y1_1,x2_1,y2_1,coef_1=lines2[0]
        line3.append(lines2[0])
        lines2.pop(0)
        lines3 = []
        
        i = 0

        while lines2:
            x1_2,y1_2,x2_2,y2_2,coef_2 = lines2[0]
            lines3.append(lines2[0])
            lines2.pop(0)
            print(abs(coef_1),abs(coef_2),abs(abs(coef_1)-abs(coef_2)))
            if abs(abs(coef_1)-abs(coef_2))<20:
                if(abs(x1_1-x1_2)+abs(y1_1-y1_2))<30:
                    if coef_1 >0 :
                        line3[i]=[x2_2,y2_2,x2_1,y2_1,(coef_1)]
                    if coef_1<0:
                        line3[i]=[x2_1,y2_1,x2_2,y2_2,(coef_2)]
                    lines3.pop()
                
                elif(abs(x2_1-x1_2)+abs(y2_1-y1_2))<30:
                    if coef_1 >0 :
                        line3[i]=[x1_1,y1_1,x2_2,y2_2,(coef_1)]
                    if coef_1<0:
                        line3[i]=[x2_2,y2_2,x1_1,y1_1,(coef_2)]
                    lines3.pop()

                elif(abs(x2_1-x2_2)+abs(y2_1-y2_2))<30:
                    if coef_1 >0 :
                        line3[i]=[x1_1,y1_1,x1_2,y1_2,(coef_1)]
                    if coef_1<0:
                        line3[i]=[x1_2,y1_2,x1_1,y1_1,(coef_2)]
                    lines3.pop()

                elif(abs(x1_1-x2_2)+abs(y1_1-y2_2))<30:
                    if coef_1 >0 :
                        line3[i]=[x1_2,y1_2,x2_1,y2_1,(coef_1)]
                    if coef_1<0:
                        line3[i]=[x2_1,y2_1,x1_2,y1_2,(coef_2)]
                    lines3.pop()
                
        i += 1        
        lines2.extend(lines3)
    #[438, 596, 443, 451, -140], [555, 530, 566, 403, -116], [422, 770, 582, 782, 172], [520, 778, 616, 785, 103], [553, 570, 555, 537, -31], [442, 465, 453, 300, -154], [444, 449, 448, 383, -62], [464, 131, 556, 48, 9]]
    #[453, 300, 438, 596, -154], [555, 530, 566, 403, -116], [422, 770, 582, 782, 172], [553, 570, 555, 537, -31], [444, 449, 448, 383, -62], [464, 131, 556, 48, 9]]
   
   #[[423, 641, 449, 436, -179], [540, 586, 571, 410, -145], [406, 763, 620, 797, 248], [422, 647, 445, 461, -163], [447, 454, 473, 294, -134], [562, 469, 587, 295, -149], [398, 761, 541, 784, 166]]
   #[[449, 436, 445, 461, -163], [540, 586, 571, 410, -145], [406, 763, 620, 797, 248]]
   
   print(line3)
    for x1, y1, x2, y2, coef in line3:    
        cv2.line(data, (x1, y1), (x2, y2), (255, 0, 0), 3)
    #cv2.line(data, (x1, y1), (x2, y2), (255, 0, 0), 3)
    
    # Show result
    plt.imshow(data)
    #plt.imshow(data)
    plt.show()  

    #ox, oy = lidar_sim.get_observation_points(lidar_datas, angle_resolution)
    #rects, id_sets = l_shape_fitting.fitting(ox, oy)
    
    if Sens_course :
        angle,vitesse=trajectoire1(lidar_datas,lidar_number_points)
        Marche=False
    else :
        angle,vitesse,Marche=Demi_tour_narvallo(lidar_datas,lidar_number_points,Marche)

    driver.setCruisingSpeed(vitesse)
    print(angle)
    driver.setSteeringAngle(angle)
    
    State=SimulationState(driver,robot_node,trans_field,rot_field,TS)
    
    

