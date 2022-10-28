"""Voiture autonome avec utilisation
self.lidar avec WIBORS"""

import numpy as np
import random
import gym
import numpy as np
from controller import Supervisor
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from vehicle import Driver
from controller import Lidar
from controller import Field

#Programme principal
# while self.conduire.step() != -1:
#     a = random.randint(1,10)
#     rouler(a)
#     reward = evaluer()
#     #print(reward)
#     etat = observe(self.lidar, 50)
    #print(self.lidar.getNumberOfPoints())
    

#Fonction d'initialisation
def initialisation(robot) :
    INITIAL_trans = [-3, 4, 0.0195182]
    INITIAL_rot=[0.000206508, -0.349092, 0.937089 , 0.00146275]
    
    #Paramètre de la voiture (position, etc..)
    voiture_robot = robot.getFromDef("vehicle")
    trans_champs = voiture_robot.getField("translation")
    rot_champs = voiture_robot.getField("rotation")
    
    trans_champs.setSFVec3f(INITIAL_trans)
    rot_champs.setSFRotation(INITIAL_rot)

#--------------GYM----------------------------

#Création de l'environnement GYM
class WebotsGymEnvironment(Supervisor, gym.Env) :
    def __init__(self, max_episode_steps=1000):
        #super().__init__()
        self.action_space = gym.spaces.Discrete(10)
        min = np.array(4*[0.0, 0.0])
        max = np.array(4*[1000.0,1000.0])
        self.observation_space = gym.spaces.Box(min.flatten(), max.flatten(), dtype=np.float32)
#         print(self.observation_space)
        
        self.spec = gym.envs.registration.EnvSpec(id='WebotsEnv-v0', max_episode_steps=max_episode_steps)
        self.done = False
        self.state = None

        self.conduire = Driver()
        self.lidar = Lidar("lidar")
        
        
        basicTimeStep = int(self.conduire.getBasicTimeStep())
        sensorTimeStep = 4 * basicTimeStep
        
        #Capteur self.lidar
        self.lidar.enable(sensorTimeStep)
        self.lidar.enablePointCloud()
        
        #Capteur de distance
        self.capteur_avant = self.conduire.getDevice('front_center_sensor')
        self.capteur_gauche = self.conduire.getDevice('side_left_sensor')
        self.capteur_droite = self.conduire.getDevice('side_right_sensor')
        self.capteur_avant.enable(sensorTimeStep)
        self.capteur_gauche.enable(sensorTimeStep)
        self.capteur_droite.enable(sensorTimeStep)
        
        #Capteur de balise
        self.capteur_balise = self.conduire.getDevice('capteur_balise')
        self.capteur_balise.enable(sensorTimeStep)
    
            
    #Vérification de l'état de la voiture
    #Retourner valeur [distance     angle]
#     def observe(lidar_sensor,lidar_nb_pts) :
#         pt=np.array(lidar_sensor.getRangeImage())
#         pt=pt.reshape((pt.shape[0],1))*1000
#         a=np.linspace(0,360, lidar_nb_pts)
#         a=a.reshape((a.shape[0],1))
#         datas=np.hstack((pt,a))
#         etat = np.array(datas).astype(np.float32)
#         etat_1D = etat.flatten()
#         #for i in a :
#             #if i == 'inf' :
#                 #a[i] = 0
#         #print(np.shape(a))
#         return etat_1D
        
#     #Fonction pour detection de collision
#     def evaluer():
#         recompense = 0
#         avant = capteur_avant.getValue()
#         gauche = capteur_gauche.getValue()
#         droite = capteur_droite.getValue()
#         balise = capteur_balise.getValue()
#         
#         if avant >= 900 :
#             print("Collision avant")
#             initialisation(self.conduire) #Réinitialisation de position en cas de crash
#             recompense = -10
#             done = True
#         elif (avant >= 854 and gauche >= 896) or (avant >= 696 and gauche >= 910) or gauche >= 937 :
#             print("Collision gauche")
#             initialisation(self.conduire)
#             recompense = -10
#             done = True
#         elif (avant >= 850 and droite >= 893) or (avant >= 584 and droite >= 910) or droite >= 961 :
#             print("Collision droite")
#             initialisation(self.conduire)
#             recompense = -10
#             done = True
#         elif balise > 700 :
#             done = False
#             print("Balise passée")
#             recompense = 10
#         else :
#             done = False
#             recompense = 0
#         
#         return recompense
    
#     #Fonction épisode
#     def is_done() :
#         if not done :
#             return False
#         else :
#             return True
#         
    #Affichage
    def view() :
        pass
        
    def reset(self):
        initialisation(self.conduire)
        #obs = observe(self.lidar,self.lidar.getNumberOfPoints())
        pt=np.array(self.lidar.getRangeImage())
        pt=pt.reshape((pt.shape[0],1))*1000
        a=np.linspace(0,360, self.lidar.getNumberOfPoints())
        a=a.reshape((a.shape[0],1))
        datas=np.hstack((pt,a))
        etat = np.array(datas).astype(np.float32)
        obs = etat.flatten()
        #for i in a :
            #if i == 'inf' :
                #a[i] = 0
        #print(np.shape(a))
#         print(np.shape(obs))
        return obs
    
    def step(self, action):
        #Etape
        if action == 0 :
            self.conduire.setSteeringAngle(-0.4)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 1 :
            self.conduire.setSteeringAngle(-0.1)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 2 :
            self.conduire.setSteeringAngle(0)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 3 :
            self.conduire.setSteeringAngle(0.1)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 4 :
            self.conduire.setSteeringAngle(0.4)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 5 :
            self.conduire.setSteeringAngle(-0.4)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 6 :
            self.conduire.setSteeringAngle(-0.1)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 7 :
            self.conduire.setSteeringAngle(0)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 8 :
            self.conduire.setSteeringAngle(0.1)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 9 :
            self.conduire.setSteeringAngle(0.4)
            self.conduire.setCruisingSpeed(1.8)
#         obs = observe(self.lidar, self.lidar.getNumberOfPoints())

        #Observation
        pt=np.array(self.lidar.getRangeImage())
        pt=pt.reshape((pt.shape[0],1))*1000
        a=np.linspace(0,360, self.lidar.getNumberOfPoints())
        a=a.reshape((a.shape[0],1))
        datas=np.hstack((pt,a))
        etat = np.array(datas).astype(np.float32)
        obs = etat.flatten()
        #for i in a :
            #if i == 'inf' :
                #a[i] = 0
        #print(np.shape(a))
    
        #Recompense
        recompense = 0
        avant = self.capteur_avant.getValue()
        gauche = self.capteur_gauche.getValue()
        droite = self.capteur_droite.getValue()
        balise = self.capteur_balise.getValue()
        
        if avant >= 900 :
            print("Collision avant")
            initialisation(self.conduire) #Réinitialisation de position en cas de crash
            recompense = -10
            done = True
        elif (avant >= 854 and gauche >= 896) or (avant >= 696 and gauche >= 910) or gauche >= 937 :
            print("Collision gauche")
            initialisation(self.conduire)
            recompense = -10
            done = True
        elif (avant >= 850 and droite >= 893) or (avant >= 584 and droite >= 910) or droite >= 961 :
            print("Collision droite")
            initialisation(self.conduire)
            recompense = -10
            done = True
        elif balise > 700 :
            done = False
            print("Balise passée")
            recompense = 10
        else :
            done = False
            recompense = 0
        
        reward = recompense
        
        #is done
        if not done :
            done = False
        else :
            done = True
        
        return obs, reward, done, {}
    
    def render(self, mode="human", close=False):
        view()


def main() :
    env = WebotsGymEnvironment()
    check_env(env)
    
#     # Entrainnement
    model = PPO('MlpPolicy', env, n_steps=2048, verbose=1)
    model.learn(total_timesteps=15)
    
    obs = env.reset()
    
    for _ in range(20):
        #Prédiction pour séléctionner une action à partir de l'observation
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        #print(obs, reward, done, info)
        if done:
            obs = env.reset()
            
if __name__ == '__main__':
    main()