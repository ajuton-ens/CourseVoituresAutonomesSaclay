import numpy as np

def trajectoire1(lidar_datas,lidar_number_points):

    W1=np.ones((len(lidar_datas[:int(lidar_number_points/4),0]),1))
    W2=np.ones((len(lidar_datas[int(lidar_number_points*3/4):,0]),1))
    #W=np.arange(lidar_number_points/4)
    #print(W)
    #W=-1/45*np.abs(W-45)+1.5
    #W=-1/2000000*(W-45)**4+2
    sd=np.dot(lidar_datas[:int(lidar_number_points/4),0]/1000/int(lidar_number_points/4),W1)
    sg=np.dot(lidar_datas[int(lidar_number_points*3/4):,0]/1000/int(lidar_number_points/4),W2)
    """
    if lidar_datas[int(lidar_number_points/4),0]/1000<0.35:
        angle_somme=0.5
        print('here1')
    elif lidar_datas[int(lidar_number_points*3/4),0]/1000<0.35:
        angle_somme=-0.5
        print('here2')
    elif lidar_datas[int(lidar_number_points/3),0]/1000<0.5:
        angle_somme=0.5
        print('here3')
    elif lidar_datas[int(lidar_number_points*2/3),0]/1000<0.5:
        angle_somme=-0.5
        print('here4')
    elif lidar_datas[int(lidar_number_points/6),0]/1000<0.5:
        angle_somme=0.5
        print('here5')
    elif lidar_datas[int(lidar_number_points*5/6),0]/1000<0.5:
        angle_somme=-0.5
        print('here6')
    else :
        angle_somme=float(abs(sg-sd)/((sg-sd)+0.0001)*abs(((sd-sg))))/(sd+sg)
    """
    ouverture=10
    angle_somme=float(abs(sg-sd)/((sg-sd)+0.0001)*abs(((sd-sg)))/(sd+sg))*2
    #print(angle_somme)
    svit=sum(lidar_datas[0:int(ouverture*lidar_number_points/360),0]+lidar_datas[lidar_number_points-int(ouverture*lidar_number_points/360):,0])/(2*int(ouverture*lidar_number_points/360))
    svit=svit/1e4
    #print("svit 1 :", svit)
    svit=10*((svit+0.000000001)**(1/2)+svit)
    angle=angle_somme
    print("svit 2 :", svit)
    if angle > 0.6:
        angle = 0.6
    if angle < -0.6:
        angle = -0.6
    #print(angle)
    
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