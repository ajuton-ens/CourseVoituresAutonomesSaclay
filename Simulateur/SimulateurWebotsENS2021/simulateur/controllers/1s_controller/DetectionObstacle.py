import numpy as np 

import scipy as sp
from scipy import signal
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from ransac import double_ransac_polyfit
import cv2


from skimage.transform import hough_line, hough_line_peaks,probabilistic_hough_line
from skimage.feature import canny
from skimage.draw import line
from skimage import data

from matplotlib import cm


def ClusteringLidarCloud(lidar_datas,lidar_number_points):
    r=lidar_datas[:,0]
    angle_lid=np.deg2rad(lidar_datas[:,1])
    """
    ax = plt.subplot(121,projection = "polar")
    ax.set_theta_zero_location("N")
    ax.plot(angle_lid, r,'.')
    plt.title("sans filtre")
    ax.plot([0], [0],'.r')
    """



    r=sp.ndimage.median_filter(r,size=30, mode="wrap")
    #r=gaussian_filter1d(r, 4)
    """
    ax = plt.subplot(122,projection = "polar")
    ax.set_theta_zero_location("N")
    ax.plot(angle_lid, r,'.')
    ax.plot([0], [0],'.r')
    plt.title("avec filtre")
    plt.legend()
    plt.show()"""


    #r=gaussian_filter1d(r, 4)
    X=r*np.cos(angle_lid)
    Y=r*np.sin(angle_lid)
    D=np.vstack((X,Y)).T

    L1=list(range(int(lidar_number_points/4)))
    L2=list(range(int(lidar_number_points*3/4),lidar_number_points))
    L1.reverse()
    L2.reverse()
    L2.pop()
    L=L1+L2

    cluster=[[]]
    Rcluster=[[]]
    Anglecluster=[[]]
    Datacluster=[[]]


    ClusterN=set(list(range(int(lidar_number_points/8)))
            +list(range(int(lidar_number_points*7/8),lidar_number_points)))
    ClusterE=set(range(int(lidar_number_points*6/8),int(lidar_number_points*7/8)))
    ClusterO=set(range(int(lidar_number_points*1/8),int(lidar_number_points*2/8)))

    ProbClusterN=[]
    ProbClusterE=[]
    ProbClusterO=[]

    for i in L:
        if i==0:
            cluster[0].append(i)
            Rcluster[0].append(r[i])
            Anglecluster[0].append(angle_lid[i])
            Datacluster[0].append(D[i])
        else :
            if i<int(lidar_number_points/4)-1:
                j=i-1
            elif i<=lidar_number_points-1:
                j=i-1
            elif i==0:
                j=lidar_number_points-1
            d=sum((D[i]-D[j])**2)
            if d>250000: #500**2
                cluster[-1].append(i)
                Rcluster[-1].append(r[i])
                Anglecluster[-1].append(angle_lid[i])
                Datacluster[-1].append(list(D[i]))
                cluster.append([])
                Rcluster.append([])
                Anglecluster.append([])
                Datacluster.append([])
            else:
                cluster[-1].append(i)
                Rcluster[-1].append(r[i])
                Anglecluster[-1].append(angle_lid[i])
                Datacluster[-1].append(list(D[i]))
    Ncluster=[]
    NRcluster=[]
    NAnglecluster=[]
    NDatacluster=[]
    ClustersToPop=[]
    for C in range(len(cluster)):
        if len(cluster[C])>10:
            cluster[C].pop(0)
            Rcluster[C].pop(0)
            Anglecluster[C].pop(0)
            Datacluster[C].pop(0)
            cluster[C].pop(-1)
            Rcluster[C].pop(-1)
            Anglecluster[C].pop(-1)
            Datacluster[C].pop(-1)
            Ncluster.append(cluster[C])
            NRcluster.append(Rcluster[C])
            NAnglecluster.append(Anglecluster[C])
            NDatacluster.append(Datacluster[C])
        else :
            ClustersToPop.append(C)
    
    
    for C in range(len(Ncluster)):
        ProbClusterN.append(len(set(Ncluster[C]).intersection(ClusterN))/len(ClusterN))
        ProbClusterE.append(len(set(Ncluster[C]).intersection(ClusterE))/len(ClusterE))
        ProbClusterO.append(len(set(Ncluster[C]).intersection(ClusterO))/len(ClusterO))
    
    DicoProbCluster={
        "ClusterN" : ProbClusterN,
        "ClusterE" : ProbClusterE,
        "ClusterO" : ProbClusterO 
    }
    return D,Ncluster,NRcluster,NAnglecluster,NDatacluster,DicoProbCluster

def ObstacleDetection(D,cluster):
    Obstacle_list=[]
    for c in range(len(cluster)):
        if len(cluster[c])>5 :
            startpoint=cluster[c][0]
            endpoint=cluster[c][-1]
            centerpoint=(D[startpoint]+D[endpoint])/2
            rayon=np.sum((D[startpoint]-D[endpoint])**2)**(1/2)/2
            if (np.pi * rayon**2) / len(cluster[c]) <10000 and rayon<600/2:
                Obstacle_list.append([centerpoint,rayon,c])
    return Obstacle_list

def RobustPinClusteringLidarCloud(cluster,D,ObstacleList,DicoProbCluster):
    if len(ObstacleList) != 0:
        ObstacleList=np.array(ObstacleList)
        #print("fdvqe", ObstacleList)
        for obs in ObstacleList[:,2]:
            if obs+1<=len(cluster)-1 and obs-1>=0 :
                startpoint2=cluster[obs+1][0]
                endpoint2=cluster[obs+1][-1]
                startpoint1=cluster[obs-1][0]
                endpoint1=cluster[obs-1][-1]
                """print("obs :", obs)
                print("start1",startpoint1)
                print("end1",endpoint1)
                print("start2",startpoint2)
                print("end2",endpoint2)
                print("snv",np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2))"""
                if np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2)<900:
                    #print("linkage cluster " , obs-1, " and ", obs+1)
                    DicoProbCluster["ClusterN"][obs-1] = DicoProbCluster["ClusterN"][obs+1] + DicoProbCluster["ClusterN"][obs-1] + DicoProbCluster["ClusterN"][obs] 
                    DicoProbCluster["ClusterE"][obs-1] = DicoProbCluster["ClusterE"][obs+1] + DicoProbCluster["ClusterE"][obs-1] + DicoProbCluster["ClusterE"][obs] 
                    DicoProbCluster["ClusterO"][obs-1] = DicoProbCluster["ClusterO"][obs+1] + DicoProbCluster["ClusterO"][obs-1] + DicoProbCluster["ClusterO"][obs] 
    for c in range(len(cluster)) :
        if c+1<=len(cluster)-1 :
            startpoint2=cluster[c+1][0]
            endpoint1=cluster[c][-1]
            if len(ObstacleList) != 0:
                if c not in np.array(ObstacleList)[:,2] and c+1 not in np.array(ObstacleList)[:,2]:
                    print(np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2))
                    if np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2)<900:
                        print("linkage cluster " , c, " and ", c+1)
                        DicoProbCluster["ClusterN"][c] =  DicoProbCluster["ClusterN"][c] + DicoProbCluster["ClusterN"][c+1] 
                        DicoProbCluster["ClusterE"][c] =  DicoProbCluster["ClusterE"][c] + DicoProbCluster["ClusterE"][c+1] 
                        DicoProbCluster["ClusterO"][c] =  DicoProbCluster["ClusterO"][c] + DicoProbCluster["ClusterO"][c+1] 
            else :
                print(np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2))
                if np.sum((D[startpoint2]-D[endpoint1])**2)**(1/2)<900:
                    print("linkage cluster " , c, " and ", c+1)
                    DicoProbCluster["ClusterN"][c] =  DicoProbCluster["ClusterN"][c+1] + DicoProbCluster["ClusterN"][c] 
                    DicoProbCluster["ClusterE"][c] =  DicoProbCluster["ClusterE"][c+1] + DicoProbCluster["ClusterE"][c] 
                    DicoProbCluster["ClusterO"][c] =  DicoProbCluster["ClusterO"][c+1] + DicoProbCluster["ClusterO"][c] 
    #print(DicoProbCluster)
    return DicoProbCluster

def ObstacleAndWallDetectionDebug(lidar_datas,lidar_number_points,L):
    D,cluster,Rcluster,Anglecluster,Datacluster,DicoProbCluster=ClusteringLidarCloud(lidar_datas,lidar_number_points)
    Obstacle_list=[]
    ax=plt.subplot(111)
    print("nex")
    for c in range(len(cluster)):
        if len(np.array(Datacluster[c]))>1 :
            #print("kjvbnksv", cluster[c])
            x=np.array(Datacluster[c])[:,0]
            y=np.array(Datacluster[c])[:,1]
            
            startpoint=cluster[c][0]
            endpoint=cluster[c][-1]
            centerpoint=(D[startpoint]+D[endpoint])/2
            rayon=np.sum((D[startpoint]-D[endpoint])**2)**(1/2)/2
            ax.plot(x, y,'.',label=("taille cluster : " +str(len(x))
                                +"\n prob clusterN : "+str(DicoProbCluster["ClusterN"][c])
                                +"\n prob clusterO : "+str(DicoProbCluster["ClusterO"][c])
                                +"\n prob clusterE : "+str(DicoProbCluster["ClusterE"][c])
                                +"\n densité : "+ str((np.pi * rayon**2) / len(np.array(Datacluster[c])[:,0]))
                                +"\n rayon : "+ str(rayon))
                                +"\n first :" + str(cluster[c][0])
                                +"\n last :" + str(cluster[c][-1]))
            #print(len(x))
            #print("densité :", (np.pi * rayon**2) / len(np.array(Datacluster[c])[:,0]))
            #print("rayon : ",rayon)
            if (np.pi * rayon**2) / len(cluster[c]) <10000 and rayon<600/2:
                #print("rayon : ",rayon)
                circle=plt.Circle((centerpoint[0],centerpoint[1]),rayon,color='y')
                ax.add_patch(circle)
                x=np.array(Datacluster[c])[:,0]
                y=np.array(Datacluster[c])[:,1]
                Obstacle_list.append([centerpoint,rayon])
                #print("densité :", (np.pi * rayon**2) / len(np.array(Datacluster[c])[:,0]))
                #print("rayon :", rayon)
            else:
                """vec_poly,inliners,err=double_ransac_polyfit(x, y, order=1, n1=2, n2=2, k1=10,k2=10, t=30, d1=len(x)/3, d2=len(x)/5)
                
                X_start=int(min(x))
                X_end=int(max(x))
                X_plot=np.linspace(X_start,X_end,100)
                #print(vec_poly)
                if len(vec_poly)==3:
                    poly1=np.poly1d(vec_poly[0])
                    poly2=np.poly1d(vec_poly[1])
                    poly3=np.poly1d(vec_poly[2])
                    plt.plot(X_plot,poly1(X_plot),'g',label='poly1')
                    plt.plot(X_plot,poly2(X_plot),'r',label='poly2')
                    plt.plot(X_plot,poly3(X_plot),'b',label='poly3')
                    plt.plot([],[],'w',label=str(err))
                elif len(vec_poly)==2:
                    poly1=np.poly1d(vec_poly[0])
                    poly2=np.poly1d(vec_poly[1])
                    plt.plot(X_plot,poly1(X_plot),'g',label='poly1')
                    plt.plot(X_plot,poly2(X_plot),'r',label='poly2')
                elif len(vec_poly)==1 and vec_poly[0][0]!=None:
                    poly=np.poly1d(vec_poly[0])
                    plt.plot(X_plot,poly(X_plot),'y',label='Poly seul')
                """
                pass
    
    plt.plot([0],[0],'or')
    ax.set_xlim(-500,5000)
    ax.set_ylim(-5000,5000)
    #print(len(Obstacle_list))
    if len(Obstacle_list)>-1:
        #plt.legend()
        plt.grid()
        #plt.show()
        plt.pause(.00001)
        ax.clear()
        
    else:
        ax.clear()
    
    return Obstacle_list


def AvoidObstacle(ObstacleList,cluster,D,angle):
    DistNearestObstacle=np.inf
    DistGauche=np.inf
    DistDroite=np.inf
    for O in ObstacleList:
        if O[2]+1<=len(cluster)-1 and O[2]-1>=0 :
            alpha=np.arctan(O[0][1]/O[0][0])
            Distance=sum(O[0]**2)**(1/2)
            print("Distance :",Distance)
            if Distance<3000 and Distance<DistNearestObstacle and alpha<np.pi/3 and alpha>-np.pi/3 :
                startpoint=cluster[O[2]][0]
                endpoint=cluster[O[2]][-1]
                for C in range(O[2]+1,len(cluster)):
                    for p in np.array(cluster[C])[np.arange(0,len(cluster[C]),10,dtype=int)]:
                        Distp=sum((D[endpoint]-D[p])**2)**(1/2)
                        if Distp<DistDroite:
                            DistDroite=Distp
                for C in range(O[2]):
                    for p in np.array(cluster[C])[np.arange(0,len(cluster[C]),10,dtype=int)]:
                        Distp=sum((D[startpoint]-D[p])**2)**(1/2)
                        if Distp<DistGauche:
                            DistGauche=Distp
                print("dg :",DistGauche)
                print("dd :",DistDroite)
                theta = np.arctan((2*O[1]+200)/(sum(O[0]**2)**(1/2)))
                if -angle < alpha+theta and -angle > alpha-theta :
                    DistNearestObstacle=Distance
                    if Distance>100:
                        if DistGauche>DistDroite:
                            angle = -(alpha+theta)
                            print("angle1 :", angle)
                        else :
                            angle = -(alpha-theta)
                            print("angle2 :", angle)
                    else:
                        if O[0][1]>0: #On est à drouate
                           print("ddddddd : ",(DistDroite/2+O[1])+O[0][1])
                           print("d2d2d2 : ",O[0][0])
                           angle = np.arctan(((DistDroite/2+O[1])+O[0][1])/abs(O[0][0]))
                           print("on est à l'aiiiiise à drouate, l'angle est :", angle)
                        else : #On est à gôche
                           print("ggggggg : ",(DistDroite/2+O[1])+O[0][1])
                           print("g2g2g2 : ",O[0][0])
                           angle = np.arctan(((DistDroite/2+O[1])+O[0][1])/abs(O[0][0]))
                           print("on est à l'aiiiiise à goche, l'angle est :", angle)
                    print("NOOOOOOON")
    print("fin")

    return angle