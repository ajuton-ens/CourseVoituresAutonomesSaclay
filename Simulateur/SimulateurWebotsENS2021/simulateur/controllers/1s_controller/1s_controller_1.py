import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import cmath as cm
import time
#from iterative_closest_point import icp_matching
import field


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



speed = 3
angle = 0


maxSpeed = 8

driver.setSteeringAngle(angle)
driver.setCruisingSpeed(speed)
for _ in range(5):
    lidar_datas=GetLidarDatas(lidar,lidar_number_points)
    lidar_cloud=lidar.getPointCloud()
    rot=robot_node.getOrientation()
    [xo,yo,zo]=robot_node.getPosition()

    cloud=[lidar_cloud[i] for i in range(1,lidar_number_points,2)]
    landmark_X=np.array([[pt.x] for pt in cloud])
    landmark_Z=np.array([[pt.z] for pt in cloud])
    landmark=np.hstack((landmark_X,landmark_Z))
    b=cm.phase(complex(rot[0],rot[2]))
    rot=np.array([[np.cos(b),-np.sin(b)],[np.sin(b),np.cos(b)]])
    landmark_rot=np.array([np.dot(lm,rot) for lm in landmark])+[xo,zo]
    previous_icp_point=landmark_rot.T

xEst=[xo,zo]
i=0
angle1=0
angle2=0
angle3=0
angle4=0

while driver.step() != -1:

    if i<=100 : i+=1

    Green_wall,Red_wall=GetPixyDatas(camera,cam_width,cam_height,Verbose=False)
    
    previous_lidar_cloud=lidar_cloud

    lidar_cloud=lidar.getPointCloud()
    [x,y,z]=robot_node.getPosition()
    rot=robot_node.getOrientation()
    
    b=cm.phase(complex(rot[0],rot[2]))
    cloud=[lidar_cloud[i] for i in range(1,lidar_number_points,2)]
    landmark_X=np.array([[pt.x] for pt in cloud])
    landmark_Z=np.array([[pt.z] for pt in cloud])
    landmark=np.hstack((landmark_X,landmark_Z))
    rot=np.array([[np.cos(b),-np.sin(b)],[np.sin(b),np.cos(b)]])
    landmark_rot=np.array([np.dot(lm,rot) for lm in landmark])+[x,z]
    icp_point=landmark_rot.T
    
    R,T=icp_matching(previous_icp_point,icp_point)
    previous_icp_point=icp_point

    lidar_datas=GetLidarDatas(lidar,lidar_number_points)
    
    index_gauche =int(lidar_number_points*5/6)
    index_droite = int(lidar_number_points/6)
    dist_gauche=lidar_datas[index_gauche][0]/1000
    dist_droite=lidar_datas[index_droite][0]/1000
    ang_gauche=lidar_datas[index_gauche][1]
    ang_droite=lidar_datas[index_droite][1]


    speed = 3

    angle = abs(dist_gauche-dist_droite)/((dist_gauche-dist_droite)+0.0001)*abs(((dist_droite-dist_gauche)))

    W=np.ones((int(lidar_number_points/4)-10,1))
    sd=np.dot(lidar_datas[10:int(lidar_number_points/4),0]/1000/int(lidar_number_points/4),W)
    sg=np.dot(lidar_datas[int(lidar_number_points*3/4):-10,0]/1000/int(lidar_number_points/4),W)
    print(sd,sg)
    angle_somme=float(abs(sg-sd)/((sg-sd)+0.0001)*abs(((sd-sg))))
    print("angle somme :",angle_somme)

    svit=sum(lidar_datas[0:10,0]+lidar_datas[lidar_number_points-10:,0])
    svit=svit/1e4
    print(svit)
    Vtang=speed*np.cos(angle)
    Vnorm=speed*np.sin(angle)

    dist_lid=lidar_datas[:,0]
    angle_lid=np.deg2rad(lidar_datas[:,1])
    
    X=dist_lid*np.cos(angle_lid)
    Y=dist_lid*np.sin(angle_lid)
    """
    ax = plt.subplot(111,projection = "polar")
    ax.plot(angle_lid, dist_lid,'.')
    ax.plot([0], [0],'.r')
    ax.plot(np.deg2rad(np.array([ang_gauche,ang_droite])), [dist_gauche*1000,dist_droite*1000],'.r')
    plt.show()
    """
    """
    ax = plt.subplot(111)
    ax.set_xlim(-10*1000,10*1000)
    ax.set_ylim(-10*1000,10*1000)
    ax.plot(X, Y,'.')
    ax.plot([0], [0],'.r')
    plt.show()
    """
    obstacle_list=np.vstack((X,Y)).T

    Field = field.E_repulsive(obstacle_list)+field.E_attractive(0,0)
    Norm_Field=np.array(Field)/((Field[0]**2+Field[1]**2)**(1/2)+1e-11) 
    #print(Norm_Field)
    Vtang_field=Norm_Field[0]*speed
    Vnorm_field=Norm_Field[1]*speed
    
    #angle=cm.phase(complex(Norm_Field[1],Norm_Field[0]))
    
    angle_field=-(cm.phase(complex(Vnorm,Vtang))-np.pi/2)
    speed=np.hypot(Vtang,Vnorm)
    
    if i>=10:
        #print("angle :",angle)
        #print("angle field :" , angle_field)
        if abs(np.cos(angle - angle_field))>np.pi/3:
            angle=angle_field
            print("switch")
        angle=(angle_somme+angle1)/2
        angle=angle_somme
        if angle > 0.8:
            angle = 0.8
        if angle < -0.8:
            angle = -0.8
        print("anglesat :", angle)
        
        if svit > 8:
            svit = 8
        if svit < -8:
            svit = -8
        print(svit)

        angle1=angle
        #print("obstacle_list :",obstacle_list)
        #field.trace_E_U(obstacle_list)
        driver.setCruisingSpeed(svit)
        driver.setSteeringAngle(angle)
        #print(T)
        #print(icp_point)
        #print(xEst)
        xEst=np.array(xEst)+np.array([T[0],T[1]])

    State=SimulationState(driver,robot_node,trans_field,rot_field,TS)
    

    if State !=None : print(State)
    if Verbose_race:
        ax_race.clear()
        landmark_X=landmark_rot.T[0]
        landmark_Z=landmark_rot.T[1]
        ax_race.plot(landmark_X, landmark_Z, '.k')
        ax_race.plot(x, z, '.r')
        ax_race.plot(np.array(xEst).T[0],np.array(xEst).T[1],'.g')
        ax_race.imshow(img, extent=[-5, 5, 5, -5])
        
        plt.pause(.00001)
    
