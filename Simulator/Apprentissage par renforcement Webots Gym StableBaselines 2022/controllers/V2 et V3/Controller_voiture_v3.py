"""Voiture autonome avec utilisation
LIDAR avec WIBORS"""

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
# while conduire.step() != -1:
#     
#     etat = observe(lidar)
#     if etat[4]<etat[31] :
#         a = 6
#     else :
#         a = 10
#     rouler(a)
#     reward = evaluer()
#     #print(reward)
#     
#     #print(etat)
#     print(lidar.getRangeImage())



#--------------GYM----------------------------

#Création de l'environnement GYM
class WebotsGymEnvironment(Supervisor, gym.Env) :
    def __init__(self):
        self.action_space = gym.spaces.Discrete(10)
        min = np.zeros(36)
        max = np.ones(36)
        self.observation_space = gym.spaces.Box(-max, max, dtype=np.float32)
        
        self.super().conduire = Driver()
        self.lidar = Lidar("lidar")

        #Paramètre de la voiture (position, etc..)
        self.voiture_robot = self.conduire.getFromDef("vehicle")
        self.trans_champs = self.voiture_robot.getField("translation")
        self.rot_champs = self.voiture_robot.getField("rotation")


        basicTimeStep = int(self.conduire.getBasicTimeStep())
        sensorTimeStep = 4 * basicTimeStep

        #Capteur LIDAR
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
    def observe(self) :
        try :
            tablo = self.lidar.getRangeImage()
            etat = np.divide(np.array(tablo),10)
        except :
            print("pas de retour du lidar")
            etat = np.zeros(36)
        return np.array(etat).astype('float32')    
        
        
    def reset(self):
        #Fonction d'initialisation
        INITIAL_trans = [-3, 4, 0.0195182]
        INITIAL_rot=[0.000206508, -0.349092, 0.937089 , 0.00146275]
        self.trans_champs.setSFVec3f(INITIAL_trans)
        self.rot_champs.setSFRotation(INITIAL_rot)
        obs = self.observe()
        #print(obs)
        return obs
    
    #Fonction pour detection de collision
    def evaluer(self):
        recompense = 0
        avant = self.capteur_avant.getValue()
        gauche = self.capteur_gauche.getValue()
        droite = self.capteur_droite.getValue()
        balise = self.capteur_balise.getValue()
        
        if avant >= 900 :
            print("Collision avant")
            self.reset() #Réinitialisation de position en cas de crash
            recompense = -10
            done = True
        elif (avant >= 854 and gauche >= 896) or (avant >= 696 and gauche >= 910) or gauche >= 937 :
            print("Collision gauche")
            self.reset()
            recompense = -10
            done = True
        elif (avant >= 850 and droite >= 893) or (avant >= 584 and droite >= 910) or droite >= 961 :
            print("Collision droite")
            self.reset()
            recompense = -10
            done = True
        elif balise > 700 :
            done = False
            print("Balise passée")
            recompense = 10
        else :
            done = False
            recompense = 0       
        return recompense, done
    
    def step(self, action):
        if action == 1 :
            self.conduire.setSteeringAngle(-0.4)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 2 :
            self.conduire.setSteeringAngle(-0.1)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 3 :
            self.conduire.setSteeringAngle(0)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 4 :
            self.conduire.setSteeringAngle(0.1)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 5 :
            self.conduire.setSteeringAngle(0.4)
            self.conduire.setCruisingSpeed(0.8)
        elif action == 6 :
            self.conduire.setSteeringAngle(-0.4)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 7 :
            self.conduire.setSteeringAngle(-0.1)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 8 :
            self.conduire.setSteeringAngle(0)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 9 :
            self.conduire.setSteeringAngle(0.1)
            self.conduire.setCruisingSpeed(1.8)
        elif action == 10 :
            self.conduire.setSteeringAngle(0.4)
            self.conduire.setCruisingSpeed(1.8)
        obs = self.observe()
        print(obs)
        print(np.shape(obs))
        reward,done = self.evaluer()
        return obs, reward, done, {}
    
    def render(self, mode="human", close=False):
        pass
    
def main() :
    env = WebotsGymEnvironment()
    check_env(env)
    
#     # Entrainnement
    model = PPO('MlpPolicy', env, n_steps=2048, verbose=1)
    model.learn(total_timesteps=1e5)
    
    obs = env.reset()
    
    for _ in range(20):
        #Prédiction pour séléctionner une action à partir de l'observation
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        #print(obs, reward, done, info)
        if done:
            obs = env.reset()
            
if __name__ == '__main__' :
    main()