"""Voiture autonome avec utilisation d'un
LIDAR sur WEBOTS
Auteur : Chrysanthe et Jessica
"""

import numpy as np
import random
import gym
import time

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from vehicle import Driver
from controller import Lidar
from controller import Field
from controller import Supervisor


#--------------GYM----------------------------

#Création de l'environnement GYM
class WebotsGymEnvironment(Driver, gym.Env) :
    def __init__(self):
        super().__init__() #Objet héritant la classe Driver
                
        basicTimeStep = int(super().getBasicTimeStep())
        self.sensorTime = basicTimeStep//4
        
        #Lidar
        self.lidar = Lidar("lidar")
        
        #Capteur LIDAR
        self.lidar.enable(self.sensorTime)
        self.lidar.enablePointCloud()
        
        self.action_space = gym.spaces.Discrete(5) #actions disponibles
        
        min = np.zeros(self.lidar.getNumberOfPoints())
        max = np.ones(self.lidar.getNumberOfPoints())
        self.observation_space = gym.spaces.Box(min, max, dtype=np.float32) #Etat venant du LIDAR
        

        #Paramètre de la voiture (position, etc..)
        self.voiture_robot = super().getFromDef("vehicle")
        self.trans_champs = self.voiture_robot.getField("translation")
        self.rot_champs = self.voiture_robot.getField("rotation")


        #Capteur de distance
        self.capteur_avant = super().getDevice('front_center_sensor')
        self.capteur_gauche = super().getDevice('side_left_sensor')
        self.capteur_droite = super().getDevice('side_right_sensor')
        self.capteur_avant.enable(self.sensorTime)
        self.capteur_gauche.enable(self.sensorTime)
        self.capteur_droite.enable(self.sensorTime)

        #Capteur de balise
        self.capteur_balise = super().getDevice('capteur_balise')
        self.capteur_balise.enable(self.sensorTime)
 
    #Vérification de l'état de la voiture
    def observe(self) :
        try :
            tableau = self.lidar.getRangeImage()
            #Division par 10 pour que la valeur soient entre 0 et 1
            etat = np.divide(np.array(tableau),10)
            print("etat : " + etat)
        except : #En cas de non retour lidar
            print("Pas de retour du lidar")
            etat = np.zeros(self.lidar.getNumberOfPoints())

        return np.array(etat).astype('float32')
    
    #Remise à 0
    def initialisation(self) :
        #self.capteur_avant.disable()
        #self.capteur_gauche.disable()
        #self.capteur_droite.disable()
        
        #Valeur aléatoire
        x = random.uniform(1.5, 1.65)
        y = random.uniform(3.66, 3.8)
            
        #Fonction d'initialisation
        INITIAL_trans = [x, y, 0.0195182]
        INITIAL_rot=[-0.000257, 0.000618, 1 , -0.784]
        self.trans_champs.setSFVec3f(INITIAL_trans)
        self.rot_champs.setSFRotation(INITIAL_rot)
        
        time.sleep(0.3) #Temps de pause après réinitilialisation
        
        #self.capteur_avant.enable(self.sensorTime)
        #self.capteur_gauche.enable(self.sensorTime)
        #self.capteur_droite.enable(self.sensorTime)
        
    #Remise à 0 pour l'environnement GYM
    def reset(self):
        self.initialisation()
        #Retour état
        obs = self.observe()
        #super().step()
        return obs
    
    #Fonction pour detection de collision et attribution des récompenses
    def evaluer(self):
        recompense = 0
        done = False
        
        avant = self.capteur_avant.getValue()
        gauche = self.capteur_gauche.getValue()
        droite = self.capteur_droite.getValue()
        balise = self.capteur_balise.getValue()
        
        if avant >= 900 and not(done) :
            print("Collision avant")
            recompense = -100
            done = True
        elif ((avant >= 854 and gauche >= 896) or (avant >= 696 and gauche >= 910) or gauche >= 937) and not(done) :
            print("Collision gauche")
            recompense = -100
            done = True
        elif ((avant >= 850 and droite >= 893) or (avant >= 584 and droite >= 910) or droite >= 961) and not(done) :
            print("Collision droite")
            recompense = -100
            done = True
        elif balise > 700 :
            done = False
            print("Balise passée")
            recompense = 200
        else :
            done = False
            recompense = 0
        
        return recompense, done
    
    #Fonction pour déplacer la voiture
    def rouler(self, action) :
        super().setCruisingSpeed(1.0)
        
        if action == 0 :
            super().setSteeringAngle(-0.4)
            
        elif action == 1 :
            super().setSteeringAngle(-0.1)
            
        elif action == 2 :
            super().setSteeringAngle(0)
            
        elif action == 3 :
            super().setSteeringAngle(0.1)
            
        elif action == 4 :
            super().setSteeringAngle(0.4)
    
    #Fonction step de l'environnement GYM
    def step(self, action):
        self.rouler(action)
        
        obs = self.observe()
        
        reward, done = self.evaluer()
        
        super().step()
        
        return obs, reward, done, {}
    
    #Fonction render de l'environnement GYM
    def render(self, mode="human", close=False):
        pass
    
    
#----------------Programme principal--------------------
def main() :
    env = WebotsGymEnvironment()
    check_env(env)
    
    logdir = "./Webots_tb/" 
    #-- , tensorboard_log = logdir -- , tb_log_name = "PPO_voiture_webots"
    
    #Définition modèle avec paramètre par défaut
    model = PPO('MlpPolicy', env, 
                n_steps = 256,
                ent_coef = 0.01,
                n_epochs = 5,
                batch_size= 32,
                learning_rate= 3e-3,
                verbose=1)
    
    #Entrainnement
    model.learn(total_timesteps=1e6)
    
    #Sauvegarde
    model.save("Voiture_autonome_Webots_PPO")
    
    #del model
    
    #Chargement des données d'apprentissage
    #model = PPO.load("Voiture_autonome_Webots_PPO")
    
    obs = env.reset()
  
    for _ in range(1000000):
        #Prédiction pour séléctionner une action à partir de l'observation
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if done:
            obs = env.reset()
  

if __name__ == '__main__' :
    main()

