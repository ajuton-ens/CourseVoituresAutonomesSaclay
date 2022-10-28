# -*-coding:Latin-1 -* 
import math as m
import numpy as np
import matplotlib.pyplot as plt        # visualisation graphique des données
import matplotlib.gridspec as gridspec # to specified a grid on figure
import mpl_toolkits.mplot3d    
import matplotlib.patches as patches
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
r=20/10**6
kappa_goal = 5/10000
x_goal=200
y_goal=0
kappa_obstacle = 0.20
x=0
y=0
#Ce script ne joue pas de rôle dans la stratégie, cependant il a été utilisé pour son
#devellopement
def E_repulsive(obstacle_list):
    
    Ex, Ey = 0, 0
    kappa_obstacle =1
    for obstacle in obstacle_list:
        x_obstacle = obstacle[0]
        y_obstacle = obstacle[1]
        
        distance_obstacle = m.hypot(x-x_obstacle, y-y_obstacle)
        
        # Les potentiels répulsifs sont des gaussiennes
        Ex += kappa_obstacle*2*r*np.exp(-r*(distance_obstacle)**2)*(x-x_obstacle)
        Ey += kappa_obstacle*2*r*np.exp(-r*(distance_obstacle)**2)*(y-y_obstacle)
        
        #if distance_obstacle > radius_obstacle:
         #   tmp = kappa_obstacle/distance_obstacle**3
          #  Ex += tmp * (x - x_obstacle)
          #  Ey += tmp * (y - y_obstacle)
            
    return np.array([Ex, Ey])

def E_attractive(Xgreen,Xred):
    # Le potentiel attractif est contitué de 2 cônes, si on se trouve à moins de
    # 400 mm et un autre pour les coutre distance qui est 2 fois plus pentu

    tmp =  -kappa_goal / m.hypot(x - x_goal, y - y_goal)
    Ex, Ey = tmp * (x - x_goal), tmp * (y - y_goal)

    return np.array([Ex, Ey])


#Tracé
def trace_E_U(obstacle_list):
    def draw_U_and_E(Q, U, E):
        """
        # inputs :
        #  Q: list of two soccer field meshes with coordonates 
        #   - Q[0] values of abscissa (type numpy.ndarray)
        #   - Q[1] values of ordonate (type numpy.ndarray)
        #  U: soccer field mesh with potential value (type numpy.ndarray)
        #  E: couple (vector) of two soccer field meshes or electric field 
        #   - E[0] x-coordonate value of electric field vector (type numpy.ndarray)
        #   - E[1] y-coordonate value of electric field vector (type numpy.ndarray)
        # output :
        #   - display plots on screen
        #   - fig: matploblib object with 2 plots
        """
        plt.close('all')
    
        # create and setup figure with ratio 1/3 and scaling 1 
        fig = plt.figure(figsize=plt.figaspect(1/3)*1) 
        fig.suptitle(glob_title, fontsize=16, horizontalalignment = 'center')    
        gs = gridspec.GridSpec(nrows=1, ncols=5) # split figure onto 5 cells
        
        # create a 3D draw spreading over the first 3 columns 
        ax1 = fig.add_subplot(gs[0, 0:-2], projection='3d', 
                              xlabel='x (mm)', ylabel='y (mm)')
        ax1.view_init(10, -60) # set the camera orientation
        # set interval for major tick on axis
        ax1.set_title(glob_title_1)
        ax1.xaxis.set_major_locator(MultipleLocator(500))
        ax1.yaxis.set_major_locator(MultipleLocator(500))
        #ax1.zaxis.set_major_locator(MultipleLocator(10000))
        ax1.plot_wireframe(Q[0], Q[1], U, rstride=1, cstride=1)
        """
        # create a 2 draw spreading over the 2 last columns 
        ax2 = fig.add_subplot(gs[0, 3:], aspect='equal', 
                              xlabel='x (mm)', ylabel='y (mm)')
        # set interval for major tick on axis
        ax2.set_title(glob_title_2)
        ax2.xaxis.set_major_locator(MultipleLocator(500))
        ax2.yaxis.set_major_locator(MultipleLocator(500))
        ax2.yaxis.tick_right()
        ax2.quiver(Q[0], Q[1], E[0], E[1], scale=25*np.max(np.hypot(E[0],E[1])))
           """ 
        plt.show() # display figure on screen
        
        return fig
    
    def U_mesh_att(X, Y):
        return kappa_goal *  np.hypot(X-x_goal, Y-y_goal)
          
    def E_mesh_att(X, Y):
        Distance_to_goal = np.hypot(X-x_goal, Y-y_goal)
        return -kappa_goal/Distance_to_goal * (X-x_goal, Y-y_goal)
    
    def U_mesh_rep(X, Y, obstacle_list):
        U_rep=np.zeros((len(X),len(X)))
        for obstacle in obstacle_list:
            x_obstacle = obstacle[0]
            y_obstacle = obstacle[1]
            Dist_to_center = np.hypot(X-x_obstacle, Y-y_obstacle)
            U_rep+=kappa_obstacle*np.exp(-r*(Dist_to_center)**2)
        return U_rep
        #return np.where(Dist_to_center > radius_obstable, 
         #           kappa_obstable/Dist_to_center, 
         #           kappa_obstable/radius_obstable)
        
    def E_mesh_rep(X, Y, obstacle_list):
        E_rep=0
        for obstacle in obstacle_list:
            x_obstacle = obstacle[0]
            y_obstacle = obstacle[1]
            if y_obstacle>0:
                Dist_to_center = np.hypot(X-x_obstacle, Y-y_obstacle)
                E_rep+=kappa_obstacle*2*r*np.exp(-r*(Dist_to_center)**2)*((X-x_obstacle), (Y-y_obstacle))
        return E_rep
        #return np.where(Dist_to_center > radius_obstable,
         #           (kappa_obstable/Dist_to_center**3)*(X-x_obstacle, Y-y_obstacle),
          #          0)
        
    Y=np.linspace(-2000,2000,20)
    X=np.linspace(-2000,5000,20)
    Q = np.meshgrid(X, Y)
    
    
    # ------------------------------
    #     Attractive potential
    # ------------------------------
    Uatt = U_mesh_att(Q[0], Q[1])
    Eatt = E_mesh_att(Q[0], Q[1])
    
    
    glob_title = 'Potentiel attractif conique '
    glob_title += '$U_{att}(q) = \kappa \, || \overrightarrow{q_{obstacle}q} ||$'
    glob_title_1 = 'Champ de potentiel $U_{att}(x,y)$'
    glob_title_2 = 'Champ électrique $\overrightarrow{E}_{att}(x,y)$'
    fig = draw_U_and_E(Q, Uatt, Eatt)
    #fig.savefig('potentiel_attractif_conique.png', dpi=300, format='png')
    
    # ------------------------------
    #   Cumulative potential
    # ------------------------------
    Ucumul=U_mesh_rep(Q[0],Q[1],obstacle_list)+Uatt
    Ecumul=U_mesh_rep(Q[0],Q[1],obstacle_list)+Eatt
    fig = draw_U_and_E(Q, Ucumul, Ecumul)
    #fig.savefig('superposition.png', dpi=300, format='png')
    
    plt.close('all')