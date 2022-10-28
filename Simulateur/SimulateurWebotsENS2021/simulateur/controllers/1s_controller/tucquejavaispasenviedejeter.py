"""
    ax = plt.subplot(111,projection = "polar")
    ax.set_theta_zero_location("N")
    for c in range(len(cluster)):
        ax.plot(Anglecluster[c], Rcluster[c],'.')
    ax.plot([0], [0],'.r')
    plt.show()
    """
    """
    Node1_weight=np.sum((D-np.vstack((D[1:],D[0])))**2,1)
    Node2_weight=(np.sum((D-np.vstack((D[lidar_number_points-1],D[:-1])))**2,1))
    if  Node2_weight.all()!=0 and Node1_weight.all()!=0:
        Node1_weight=1/Node1_weight
        Node2_weight=1/Node2_weight
        G=nx.Graph()

        Tuple_Nodes1=np.empty((lidar_number_points,3),dtype=object)
        #Node1_Dico_weight = [{"weight": 1/Node1_weight[i]} for i in range(lidar_number_points)]
        Tuple_Nodes1[:,0]=np.arange(lidar_number_points)
        Tuple_Nodes1[:,1]=np.hstack((np.arange(1,lidar_number_points),[0]))
        Tuple_Nodes1[:,2]=Node1_weight
        
        #Nodes1=np.vstack((np.arange(lidar_number_points),np.hstack((np.arange(1,lidar_number_points),[0]))))
        #Nodes1=np.vstack((Nodes1,Node1_Dico_weight))
        #Nodes1=np.vstack((Nodes1,Node1_weight))

        Tuple_Nodes2=np.empty((lidar_number_points,3),dtype=object)
        #Node2_Dico_weight = [{"weight":1/Node2_weight[i] } for i in range(lidar_number_points)]
        
        Tuple_Nodes2[:,0]=np.arange(lidar_number_points)
        Tuple_Nodes2[:,1]=np.hstack(([lidar_number_points-1],np.arange(lidar_number_points-1)))
        Tuple_Nodes2[:,2]=Node2_weight

        #Nodes2=np.vstack((np.arange(lidar_number_points),np.hstack(([lidar_number_points-1],np.arange(lidar_number_points-1)))))
        #Nodes2=np.vstack((Nodes2,Node2_Dico_weight))
        #Nodes2=np.vstack((Nodes2,Node2_weight))
        #Nodes=np.hstack((Nodes1,Nodes2))
        #print(Nodes1)
        #print(Nodes2)
        #Nodes=np.array(Nodes.T, dtype=[('node1', '<i4'), ('node2', '<i4'), ('weight', '<f4')])
        #print(Nodes)
        G.add_weighted_edges_from(tuple(map(tuple, Tuple_Nodes1)))
        G.add_weighted_edges_from(tuple(map(tuple, Tuple_Nodes2)))
        partition = community_louvain.best_partition(G)
        plt.figure()
        # draw the graph
        pos = nx.spring_layout(G)
        # color the nodes according to their partition
        cmap = pltcm.get_cmap('viridis', max(partition.values()) + 1)
        nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                            cmap=cmap, node_color=list(partition.values()))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()
    else:
        print("zeros in lidar datas")

    """
    """
    r=lidar_datas[:,0]
    angle_lid=np.deg2rad(lidar_datas[:,1])
    r_filt=[]
    angle_filt=[]
    for i in range(len(r)):
        if i !=359:
            j=i+1
        else:
            j=0
        r1=r[i]
        r2=r[j]
        if abs(r1-r2)>100:
            r_filt.append(r1)
            angle_filt.append(angle_lid[i])
            
    ax = plt.subplot(111,projection = "polar")
    ax.set_theta_zero_location("N")
    ax.plot(angle_lid, r,'g.')
    ax.plot(angle_filt, r_filt,'b.')
    ax.plot([0], [0],'.r')
    plt.show()
    plt.figure()
    ax = plt.subplot(111)
    ax.plot(angle_lid, r,'g.')
    ax.plot(angle_filt, r_filt,'b.')
    ax.plot([0], [0],'.r')
    plt.show()
    
    #ox, oy = lidar_sim.get_observation_points(lidar_datas, angle_resolution)
    #rects, id_sets = l_shape_fitting.fitting(ox, oy)
    """


            if len(np.array(Datacluster[c])[:,0])>20:
                startpoint=cluster[c][0]
                endpoint=cluster[c][-1]
                x=np.array(Datacluster[c])[:,0]
                y=np.array(Datacluster[c])[:,1]
                ax.plot(x, y,'.')
                vec_poly,err=ransac_polyfit(x, y, order=3, n=int(len(x)*3/4), k=10, t=100, d=0, f=0)
                poly=np.poly1d(vec_poly)
                X_start=int(min(x))
                X_end=int(max(x))
                
                X_plot=np.linspace(X_start,X_end,100)
                plt.plot(X_plot,poly(X_plot),'r')
                ax.set_xlim(-5000,5000)
                ax.set_ylim(-7000,7000)
                


    ax = plt.subplot(122,projection = "polar")
        ax.set_theta_zero_location("N")
        for c in range(len(cluster)):
            ax.plot(Anglecluster[c], Rcluster[c],'.')
        ax.plot([0], [0],'.r')
        plt.show()


            """
    if len(Rcluster)>2:
        tmp1=Rcluster.pop(0)
        tmp2=Rcluster.pop(-1)
        tmp1.reverse()
        tmp2.reverse()
        Rcluster.append(tmp1+tmp2)

        tmp1=Anglecluster.pop(0)
        tmp2=Anglecluster.pop(-1)
        tmp1.reverse()
        tmp2.reverse()
        Anglecluster.append(tmp1+tmp2)

        tmp1=cluster.pop(0)
        tmp2=cluster.pop(-1)
        tmp1.reverse()
        tmp2.reverse()
        cluster.append(tmp1+tmp2)

        tmp1=Datacluster.pop(0)
        tmp2=Datacluster.pop(-1)
        tmp1.reverse()
        tmp2.reverse()
        Datacluster.append(tmp1+tmp2)
    """


    ax=plt.subplot(121)
            plt.plot(x,y,'.')
            plt.grid()
            ax=plt.subplot(122)
            err2= np.abs(m2*x-y+b2)/np.sqrt(m2**2+1)
            err1= np.abs(m1*x-y+b1)/np.sqrt(m1**2+1)
            plt.plot(x[alsoinliers1],y[alsoinliers1],'.',label='alsoinlners1')
            plt.plot(x,np.polyval(maybemodel1, x),label='modele 1')
            plt.plot(x[outliner],y[outliner],'.',label='outliners')
            plt.plot(x[outliner][maybeinliers2],y[outliner][maybeinliers2],'y.',label='maybeinliner2')
            plt.plot(x[outliner][alsoinliers2],y[outliner][alsoinliers2],'.',label='alsoinlners2')
            plt.plot(x[outliner][alsoinliers2],np.polyval(maybemodel2, x[outliner][alsoinliers2]),label='modele 2')
            plt.plot(x[outliner][maybeinliers2],y[outliner][maybeinliers2],'y.',label='maybeinliner2')
            plt.plot([],[],'w',label="erreur = "+str(np.sum(np.minimum(err1,err2))))
            plt.grid()
            plt.legend()
            plt.show()







            """
    s1,s2=[],[]
    if angle >= 0 :
        if angle-np.deg2rad(ouverture)>0 :
            s1=lidar_datas[int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0]
            s2=[]
        else :
            s1=lidar_datas[:int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0]
            s2=lidar_datas[int(lidar_number_points+angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):,0]
    else :
        if angle+np.deg2rad(ouverture)<0 :
            s1=lidar_datas[lidar_number_points+int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360):lidar_number_points+int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360),0]
            s2=[]
        else :
            s1=lidar_datas[:-int(angle*lidar_number_points/(2*np.pi)-ouverture*lidar_number_points/360),0]
            s2=lidar_datas[lidar_number_points-int(angle*lidar_number_points/(2*np.pi)+ouverture*lidar_number_points/360):,0]
    
        """