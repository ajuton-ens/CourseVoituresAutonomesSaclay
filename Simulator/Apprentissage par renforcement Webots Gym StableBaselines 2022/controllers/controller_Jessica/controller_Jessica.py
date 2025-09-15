import numpy as np
import random
import sys
import gym
import numpy as np
from controller import Supervisor
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from vehicle import Driver
from controller import Lidar
from controller import Field

class OpenAIGymEnvironment(Supervisor, gym.Env):
    def __init__(self, max_episode_steps=1000):
        super().__init__()
        self.lidar = Lidar("lidar")
        self.action_space = gym.spaces.Discrete(10)
        min = np.zeros(36)
        max = np.ones(36)
        self.observation_space = gym.spaces.Box(min, max, dtype=np.float32)
        self.state = None
        self.spec = gym.envs.registration.EnvSpec(id='WebotsEnv-v0', max_episode_steps=max_episode_steps)

        # Environment specific
        self.__timestep = int(self.getBasicTimeStep())
        
        #Paramètre de la voiture (position, etc..)
        self.robot = self.getSelf()
        self.voiture_robot = super().getFromDef("vehicle")
        self.trans_champs = self.voiture_robot.getField("translation")
        self.rot_champs = self.voiture_robot.getField("rotation")
        
    # Observation
    def observe(self):
        
        try :
            tablo = self.lidar.getRangeImage()
            etat = np.divide(np.array(tablo),10)
        except :
            print("pas de retour du lidar")
            etat = np.zeros(36)
        print('etat=',etat)
        return np.array(etat).astype('float32') 
        
    def reset(self):
        # Reset the simulation
        self.simulationResetPhysics()
        self.simulationReset()
        super().step(self.__timestep)
        
        self.INITIAL_trans = [-3, 4, 0.0195182]
        self.INITIAL_rot=[0.000206508, -0.349092, 0.937089 , 0.00146275]
        self.trans_champs.setSFVec3f(self.INITIAL_trans)
        self.rot_champs.setSFRotation(self.INITIAL_rot)
        
        
        #lidar 
        
        self.lidar.enable(self.__timestep)
        self.lidar.enablePointCloud()
        
        #Capteurs
        #Capteur de distance
        self.capteur_avant = super().getDevice('front_center_sensor')
        self.capteur_gauche = super().getDevice('side_left_sensor')
        self.capteur_droite = super().getDevice('side_right_sensor')
        self.capteur_avant.enable(self.__timestep)
        self.capteur_gauche.enable(self.__timestep)
        self.capteur_droite.enable(self.__timestep)

        #Capteur de balise
        self.capteur_balise = super().getDevice('capteur_balise')
        self.capteur_balise.enable(self.__timestep)
        
        super().step(self.__timestep)
        obs = self.observe()
        print ('obs=',obs)
        return obs
        
    
            # Reward
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
            super().step(self.__timestep)
#             super().setSteeringAngle(-0.4)
#             super().setCruisingSpeed(0.8)

        elif action == 2 :
            super().step(self.__timestep)
#             super().setSteeringAngle(-0.1)
#             super().setCruisingSpeed(0.8)
        elif action == 3 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0)
#             super().setCruisingSpeed(0.8)
        elif action == 4 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0.1)
#             super().setCruisingSpeed(0.8)
        elif action == 5 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0.4)
#             super().setCruisingSpeed(0.8)
        elif action == 6 :
            super().step(self.__timestep)
#             super().setSteeringAngle(-0.4)
#             super().setCruisingSpeed(1.8)
        elif action == 7 :
            super().step(self.__timestep)
#             super().setSteeringAngle(-0.1)
#             super().setCruisingSpeed(1.8)
        elif action == 8 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0)
#             super().setCruisingSpeed(1.8)
        elif action == 9 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0.1)
#             super().setCruisingSpeed(1.8)
        elif action == 10 :
            super().step(self.__timestep)
#             super().setSteeringAngle(0.4)
#             super().setCruisingSpeed(1.8)
        
#         super().step(self.__timestep)
        obs = self.observe()
        reward,done = self.evaluer()
        
        return obs, reward, done, {}
    

def main():
    # Initialize the environment
    env = OpenAIGymEnvironment()
    check_env(env)

    # Train
    model = PPO('MlpPolicy', env, n_steps=2048, verbose=1)
    model.learn(total_timesteps=15)

    obs = env.reset()
    for _ in range(100000):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        print(obs, reward, done, info)
        if done:
            obs = env.reset()


if __name__ == '__main__':
    main()
        
        

        
        
        
       
    
        

        
        
