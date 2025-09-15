import numpy as np
import random
import sys
sys.path.append("../utils/")
from trajectory import load_trajectory
from collections import deque

from vehicle import Driver
from controller import Lidar
from controller import Field
from controller import Supervisor



# --------------GYM----------------------------

class CarLogic(Driver):
    """
        Abstract class handling recurrent driving logic and logging.

        One should create a class inherited from CarLogic and implement a method drive() that takes arbitrary input and
        uses the `setSpeedCommand()` and `setSteeringCommand()` to control the car.
        A minimal working example is available at `minimalController/minimalController.py`

        The class is far from perfect, be careful !
    """

    def __init__(self,
                 reset_delay=12,
                 record_list = ('steering_command','lidar_range_image','speed_command','car_position'),
                 path_to_trajectory=None,
                 rot_value=[-0.000257, 0.000618, 1, -0.784],
                 pos_value=[1.5, 3.74, 0.0195182]):
        print('Initialisation')
        super().__init__()  # Objet héritant la classe Driver

        basicTimeStep = int(super().getBasicTimeStep())
        self.sensorTime = basicTimeStep // 4

        # Lidar
        self.lidar = Lidar("lidar")

        # Capteur LIDAR
        self.lidar.enable(self.sensorTime)
        self.lidar.enablePointCloud()

        # Paramètre de la voiture (position, etc..)
        self.car = super().getFromDef("vehicle")
        self.trans_champs = self.car.getField("translation")
        self.rot_champs = self.car.getField("rotation")

        # Capteur de pression
        list_touch_sensor_name = ['touch_sensor_right','touch_sensor_back','touch_sensor_front','touch_sensor_left']

        # Look, super() need to be provided with explicit parameters here
        self.touch_sensors = {sensor_name:super(CarLogic,self).getDevice(sensor_name) for sensor_name in list_touch_sensor_name}

        [sensor.enable(self.sensorTime) for sensor in self.touch_sensors.values()]

        self.reset_delay = reset_delay

        #distance

        self.last_position = None
        self.travelled_distance = 0


        self.record_list = record_list
        self.init_full_logs()

        self.setSpeedCommand(0)
        self.setSteeringCommand(0)

        # Capteur de balise
        self.init_balises()


        self.init_spawn(path = path_to_trajectory, rot_value=rot_value, pos_value=pos_value)

    def init_empty_buffer(self, buffer_size=3):
        """

        :param buffer_size:
        :return:
        """
        self.steeringCommand_buffer = deque([], maxlen=buffer_size)
        self.speedCommand_buffer = deque([], maxlen=buffer_size)
        self.velocity_buffer = deque([], maxlen=buffer_size)

    def record_kv_episode_log(self,key,value):
        """
        Add the value to the corresponding temporary key list.
        """
        if key in self.record_list:
            self.episode_log_buffer[key].append(value)

    def reset_n_write_log(self):
        """

        TODO: Problem here if some value is not recorded in certain episods ()
        TODO: write to disk every x iterations (around 40) to prevent data issues
        """
        for k,v in self.episode_log_buffer.items():
            self.full_logs[k].append(v)

        self.episode_log_buffer = {k:[] for k in self.record_list}

    def init_full_logs(self):
        """
            helper function to initialize the log tracking system
        :return:
        """
        self.full_logs = {k:[] for k in self.record_list}
        self.episode_log_buffer = {k:[] for k in self.record_list}

    def init_balises(self):
        """
            DEPRECATED - useful when implementing lap reward.
        """

        self.capteur_balise = super().getDevice('capteur_balise')
        self.capteur_balise.enable(self.sensorTime)
        balises = []
        loop = True
        i = 1
        while loop:
            balise = self.getFromDef(f'Balise({i})')

            if balise is None:
                break
            coord = balise.getPosition()
            balises.append((coord[0], coord[1]))
            i += 1
        self.balises = balises
        self.current_advancement = set()

        print('balises: ',self.balises)

    def init_spawn(self,rot_value,pos_value,path=None): #TODO: horrible one, change that
        if path:
            print(path)
            traj = load_trajectory(path)
            self.spawn_position = traj['positions']
            self.spawn_rotation = traj['rotations']
        else:
            self.spawn_position = pos_value
            self.spawn_rotation = rot_value

    # Remise à 0
    def respawn(self,speedCommand=0,steeringCommand=0):
        """
            Respawn can be random or fixed depending on how self.spawn_position was defined.
        """
        if not isinstance(self.spawn_position[0], list):
            xp,yp,zp = self.spawn_position
            xr, yr, zr,kr = self.spawn_rotation
        else:
            k = random.randint(0,len(self.spawn_position)-1)
            xp, yp, zp = self.spawn_position[k]
            xr, yr, zr, kr = self.spawn_rotation[k]

        INITIAL_trans = [xp + random.uniform(-0.05,0.05),yp + random.uniform(-0.05,0.05),zp]
        INITIAL_rot =  [xr,yr,zr,kr]

        self.trans_champs.setSFVec3f(INITIAL_trans)
        self.rot_champs.setSFRotation(INITIAL_rot)
        self.car.setVelocity([0,0,0,0,0,0])
        self.current_advancement = set()

        self.setSteeringCommand(steeringCommand)
        self.setSpeedCommand(speedCommand)

    def reset(self, speedCommand=0, steeringCommand=0):
        """
            Reset the car and call the respawn function
        """
        self.reset_n_write_log()
        self.respawn(speedCommand=speedCommand,steeringCommand=steeringCommand)
        for i in range(self.reset_delay):
            super().step()
        x,y,_ = self.car.getPosition()
        self.last_position = (x,y)


    def setSpeedCommand(self,speed_command):
        """
            Set the speed command of the car. Record the value if needed
        """
        super().setCruisingSpeed(speed_command)

        self.speedCommand = speed_command
        self.record_kv_episode_log('speed_command',speed_command)


    def setSteeringCommand(self,steeringCommand):
        """
            Set the steering command of the car. Record the value if needed
        """
        super().setSteeringAngle(steeringCommand)
        self.steeringCommand = steeringCommand
        self.record_kv_episode_log('steering_command',steeringCommand)

    def get_square_speed(self):
        """
            Get the squared speed of the car
        :return:
        """
        return (np.array(self.car.getVelocity()[:3])**2).sum()

    def get_speed_vector(self,normalized = False):
        """
            Get the speed vector of the car along x y z.
        :param normalized:
        :return:
        """
        if normalized:
            return (np.array(self.car.getVelocity()[:3])+1)/2
        else:
            return np.array(self.car.getVelocity()[:3])

    def get_normalized_lidar_range_image(self):
        """
            Return the lidar range image with value between 0 and 1. inf values are set to 1.
        """
        tableau = self.lidar.getRangeImage()
        etat = np.divide(np.array(tableau), 10)
        etat[~np.isfinite(etat)] = 1
        self.record_kv_episode_log('lidar_range_image', etat.tolist())

        return etat

    def update_travelled_distance(self):
        """
        A recorder for the total travelled distance. Also usefull to update last position
        """
        x,y,_ = self.car.getPosition()
        self.record_kv_episode_log('car_position', (x,y))
        xp,yp = self.last_position
        self.travelled_distance += np.sqrt((x-xp)**2+(y-yp)**2)
        self.last_position = (x,y)

    def get_collision(self):
        """
        Test all touch sensors to detect a possible collision
        :return:
        """
        for name,sensor in self.touch_sensors.items():
            if sensor.getValue() != 0.0:
                print(f"Colision detected : {name}")
                return True
        return False

    def check_bug(self):
        """
        Verify if something strange is happening physic wise. If so, return True to reset the simulation.
        :return:
        """
        x, y, _ = self.car.getPosition()
        xp, yp = self.last_position
        bug_threshold = 20
        if np.sqrt((x-xp)**2+(y-yp)**2) > bug_threshold:
            return True

        bug_velocity_threshold = 40 #TODO: parametrize this at class level

        if (np.array(self.car.getVelocity()[:3])**2).sum()>bug_velocity_threshold:
            return True
        return False

    def get_balise(self):
        """
        DEPRECATED - useful when implementing lap reward.
        """
        balise = self.capteur_balise.getValue()
        if balise > 700:
            return self.get_balise_id()
        return None

    def update_advancement(self, id):
        """
        DEPRECATED - useful when implementing lap reward.
        """
        if not id is None and id not in self.current_advancement:
            self.current_advancement.add(id)
            if len(self.current_advancement) >= len(self.balises):
                self.current_advancement = set()
                print("Un tour !")
                return True
            else:
                print(f"Balise {id} passée")
                return True
        return False

    def render(self, mode="human", close=False):
        pass

    def get_balise_id(self):
        """
        DEPRECATED - useful when implementing lap reward.
        """
        car_pos = self.car.getPosition()
        dist = list(map(lambda x: (x[0]-car_pos[0])**2 + (x[1]-car_pos[1])**2, self.balises))
        return dist.index(min(dist))


def main():
    pass

if __name__ == '__main__':
    main()

