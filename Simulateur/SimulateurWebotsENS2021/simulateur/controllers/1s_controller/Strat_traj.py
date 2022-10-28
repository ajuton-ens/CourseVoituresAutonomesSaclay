import numpy as np
from DetectionObstacle import ClusteringLidarCloud,RobustPinClusteringLidarCloud,ObstacleDetection,AvoidObstacle

def trajectoire1(lidar_datas,lidar_number_points):

    W1=np.ones((len(lidar_datas[:int(lidar_number_points/4),0]),1))
    W2=np.ones((len(lidar_datas[int(lidar_number_points*3/4):,0]),1))
    #W=np.arange(lidar_number_points/4)
    #print(W)
    #W=-1/45*np.abs(W-45)+1.5
    #W=-1/2000000*(W-45)**4+2
    sd=np.dot(lidar_datas[:int(lidar_number_points/4),0]/1000/int(lidar_number_points/4),W1)
    sg=np.dot(lidar_datas[int(lidar_number_points*3/4):,0]/1000/int(lidar_number_points/4),W2)
    ouverture=10
    angle_somme=float(abs(sg-sd)/((sg-sd)+0.0001)*abs(((sd-sg)))/(sd+sg))*2
    #print(angle_somme)
    angle=angle_somme
    if angle > 0.6:
        angle = 0.6
    if angle < -0.6:
        angle = -0.6
    #print("angle :" ,angle)

    S1,S2=0,0
    if angle >= 0 :
        if angle-np.deg2rad(ouverture)>0 :
            S1=sum(lidar_datas[int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=0
        else :
            S1=sum(lidar_datas[:int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=sum(lidar_datas[int(lidar_number_points+angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):,0])
    else :
        if angle+np.deg2rad(ouverture)<0 :
            S1=sum(lidar_datas[lidar_number_points+int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):lidar_number_points+int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=0
        else :
            S1=sum(lidar_datas[:-int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360),0])
            S2=sum(lidar_datas[lidar_number_points-int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360):,0])
    
    
    svit=S1+S2
    svit=svit/(2*int(ouverture*lidar_number_points/360))
    
    #svit=lidar_datas[int(angle*lidar_number_points/(2*np.pi)),0]
    svit=svit/1e4
    svit=12*((svit+0.000000001)**(1/2)+svit)
    return(angle,svit)

def Demi_tour_narvallo(lidar_datas,lidar_number_points,Marche):
    ouverture=5
    somme_ar = sum(lidar_datas[int(lidar_number_points/2)-int(ouverture*lidar_number_points/360):int(lidar_number_points/2)+int(ouverture*lidar_number_points/360),0])/(2*int(ouverture*lidar_number_points/360))
    somme_av = (sum(lidar_datas[lidar_number_points-int(ouverture*lidar_number_points/360):lidar_number_points,0])+sum(lidar_datas[0:int(ouverture*lidar_number_points/360),0]))/(2*int(ouverture*lidar_number_points/360))
    if somme_ar > 700 and not(Marche):
        angle=-0.6
        vitesse = -3 
        print("ar")
    elif somme_av > 400 and Marche:
        angle = 0.6
        vitesse = 3
        print("av")
    else :
        angle = 0
        vitesse = 0 
        Marche = not(Marche)
        print("nein")
    print(somme_ar)
    print(somme_av)
    return angle, vitesse, Marche


def trajectoire2(lidar_datas,lidar_number_points,VirageDroiteSerre,VirageGaucheSerre):

    W1=np.ones((len(lidar_datas[:int(lidar_number_points/4),0]),1))
    W2=np.ones((len(lidar_datas[int(lidar_number_points*3/4):,0]),1))
    #W=np.arange(lidar_number_points/4)
    #print(W)
    #W=-1/45*np.abs(W-45)+1.5
    #W=-1/2000000*(W-45)**4+2
    sd=np.dot(lidar_datas[:int(lidar_number_points/4),0]/1000/int(lidar_number_points/4),W1)
    sg=np.dot(lidar_datas[int(lidar_number_points*3/4):,0]/1000/int(lidar_number_points/4),W2)
    
    ouverture=10
    angle_somme=float(abs(sg-sd)/((sg-sd)+0.0001)*abs(((sd-sg)))/(sd+sg))*2
    #print(angle_somme)
    angle=angle_somme
    if angle > 0.6:
        angle = 0.6
    if angle < -0.6:
        angle = -0.6
    #print("angle :" ,angle)

    
    S1,S2=0,0
    """
    if angle >= 0 :
        if angle-np.deg2rad(ouverture)>0 :
            S1=sum(lidar_datas[int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=0
        else :
            S1=sum(lidar_datas[:int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=sum(lidar_datas[int(lidar_number_points+angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):,0])
    else :
        if angle+np.deg2rad(ouverture)<0 :
            S1=sum(lidar_datas[lidar_number_points+int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):lidar_number_points+int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0])
            S2=0
        else :
            S1=sum(lidar_datas[:-int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360),0])
            S2=sum(lidar_datas[lidar_number_points-int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360):,0])
    """
    
    svit=S1+S2
    svit=svit/(2*int(ouverture*lidar_number_points/360))
    
    #svit=lidar_datas[int(angle*lidar_number_points/(2*np.pi)),0]
    svit=svit/1e4
    svit=12*((svit+0.000000001)**(1/2)+svit)


    sld=sum(lidar_datas[int(lidar_number_points*11/16):int(lidar_number_points*13/16),0])
    slg=sum(lidar_datas[int(lidar_number_points*3/16):int(lidar_number_points*5/16),0])
    slg=slg/int(lidar_number_points*2/16)/10
    sld=sld/int(lidar_number_points*2/16)/10
    #print("slg:",slg)
    #print("sld:",sld)

    D,cluster,Rcluster,Anglecluster,Datacluster,DicoProbCluster=ClusteringLidarCloud(lidar_datas,lidar_number_points)
    ObstacleList=ObstacleDetection(D,cluster)
    DicoProbCluster=RobustPinClusteringLidarCloud(cluster,D,ObstacleList,DicoProbCluster)

    NbClusterN=DicoProbCluster["ClusterN"].index(max(DicoProbCluster["ClusterN"]))
    NbClusterO=DicoProbCluster["ClusterO"].index(max(DicoProbCluster["ClusterO"]))
    NbClusterE=DicoProbCluster["ClusterE"].index(max(DicoProbCluster["ClusterE"]))
    
    if (DicoProbCluster["ClusterE"][NbClusterN]>0.1 
        and DicoProbCluster["ClusterO"][NbClusterN]>0.7
        and VirageGaucheSerre==False) :
        VirageDroiteSerre = True
        print("epingle droite on")
    else :
        print("epingle droite off")
        VirageDroiteSerre = False
    
    if (DicoProbCluster["ClusterO"][NbClusterN]>0.1 
        and DicoProbCluster["ClusterE"][NbClusterN]>0.7
        and VirageDroiteSerre == False):
        VirageGaucheSerre = True
        print("epingle gauche on")
    else :
        VirageGaucheSerre = False
        print("epingle gauche off")
   
    if VirageDroiteSerre == True : 
        if sld > 50 :
            angle = 0.6
        else :
            angle = 0
            print("tooooo close drouate")
        print(angle)
    if VirageGaucheSerre == True :
        if slg > 50 :
            angle = -0.6
        else :
            angle = 0
            print("tooooo close gôche")
        print(angle)

    angle=AvoidObstacle(ObstacleList,cluster,D,angle)

    return(angle,svit,VirageDroiteSerre,VirageGaucheSerre)
