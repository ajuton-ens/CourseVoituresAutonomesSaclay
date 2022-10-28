# -*-coding:Latin-1 -* 
import numpy as np
import time
def GetLidarDatas(lidar,lidar_number_points):
    """
    Structures des données renvoyées :
    array :     [ distance     angle ]
                [ distance     angle ]
                          .
                          .
                          .
                [ distance     angle ]

pro tips : le 0° est à l'arrière de la voiture

    """
    pt=np.array(lidar.getRangeImage())
    pt=pt.reshape((pt.shape[0],1))*1000
    a=np.linspace(0,360,lidar_number_points)
    a=a.reshape((a.shape[0],1))
    datas=np.hstack((pt,a))
    #time.sleep(28e-3)
    return datas