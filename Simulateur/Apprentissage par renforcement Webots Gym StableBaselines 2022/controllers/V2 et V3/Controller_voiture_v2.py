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

# variable
cumul_recompense = 0
done = False

conduire = Driver()
lidar = Lidar("lidar")

#Paramètre de la voiture (position, etc..)
voiture_robot = conduire.getFromDef("vehicle")
trans_champs = voiture_robot.getField("translation")
rot_champs = voiture_robot.getField("rotation")


basicTimeStep = int(conduire.getBasicTimeStep())
sensorTimeStep = 4 * basicTimeStep

#Capteur LIDAR
lidar.enable(sensorTimeStep)
lidar.enablePointCloud()

#Capteur de distance
capteur_avant = conduire.getDevice('front_center_sensor')
capteur_gauche = conduire.getDevice('side_left_sensor')
capteur_droite = conduire.getDevice('side_right_sensor')
capteur_avant.enable(sensorTimeStep)
capteur_gauche.enable(sensorTimeStep)
capteur_droite.enable(sensorTimeStep)

#Capteur de balise
capteur_balise = conduire.getDevice('capteur_balise')
capteur_balise.enable(sensorTimeStep)

#Fonction d'initialisation
def initialisation() :
    INITIAL_trans = [-3, 4, 0.0195182]
    INITIAL_rot=[0.000206508, -0.349092, 0.937089 , 0.00146275]
    trans_champs.setSFVec3f(INITIAL_trans)
    rot_champs.setSFRotation(INITIAL_rot)

#Fonction de l'action à prendre
def rouler (action) :
    if action == 1 :
        conduire.setSteeringAngle(-0.4)
        conduire.setCruisingSpeed(0.8)
    elif action == 2 :
        conduire.setSteeringAngle(-0.1)
        conduire.setCruisingSpeed(0.8)
    elif action == 3 :
        conduire.setSteeringAngle(0)
        conduire.setCruisingSpeed(0.8)
    elif action == 4 :
        conduire.setSteeringAngle(0.1)
        conduire.setCruisingSpeed(0.8)
    elif action == 5 :
        conduire.setSteeringAngle(0.4)
        conduire.setCruisingSpeed(0.8)
    elif action == 6 :
        conduire.setSteeringAngle(-0.4)
        conduire.setCruisingSpeed(1.8)
    elif action == 7 :
        conduire.setSteeringAngle(-0.1)
        conduire.setCruisingSpeed(1.8)
    elif action == 8 :
        conduire.setSteeringAngle(0)
        conduire.setCruisingSpeed(1.8)
    elif action == 9 :
        conduire.setSteeringAngle(0.1)
        conduire.setCruisingSpeed(1.8)
    elif action == 10 :
        conduire.setSteeringAngle(0.4)
        conduire.setCruisingSpeed(1.8)
        
    
#Vérification de l'état de la voiture
#Retourner valeur [distance     angle]
def observe(lidar_sensor) :
    try :
        tablo = lidar_sensor.getRangeImage()
        etat = np.divide(np.array(tablo),10)
    except :
        print("pas de retour du lidar")
        etat = np.zeros(36)
    return np.array(etat).astype('float32')
    
#Fonction pour detection de collision
def evaluer():
    recompense = 0
    avant = capteur_avant.getValue()
    gauche = capteur_gauche.getValue()
    droite = capteur_droite.getValue()
    balise = capteur_balise.getValue()
    
    if avant >= 900 :
        print("Collision avant")
        initialisation() #Réinitialisation de position en cas de crash
        recompense = -10
        done = True
    elif (avant >= 854 and gauche >= 896) or (avant >= 696 and gauche >= 910) or gauche >= 937 :
        print("Collision gauche")
        initialisation()
        recompense = -10
        done = True
    elif (avant >= 850 and droite >= 893) or (avant >= 584 and droite >= 910) or droite >= 961 :
        print("Collision droite")
        initialisation()
        recompense = -10
        done = True
    elif balise > 700 :
        done = False
        print("Balise passée")
        recompense = 10
    else :
        done = False
        recompense = 0
    
    return recompense

#Fonction épisode
def is_done() :
    if not done :
        return False
    else :
        return True
    
#Affichage
def view() :
    pass

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
        #print(self.observation_space)
        
    def reset(self):
        initialisation()
        obs = observe(lidar)
        print(obs)
        return obs
    
    def step(self, action):
        rouler(action)
        obs = observe(lidar)
        print(obs)
        print(np.shape(obs))
        reward = evaluer()
        done = is_done()
        return obs, reward, done, {}
    
    def render(self, mode="human", close=False):
        view()


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