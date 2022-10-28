# -*-coding:Latin-1 -* 
import numpy as np

def SimulationState(driver,robot_node,trans_field,rot_field,TS):
    """
    En cas de collision cette fonction gère l'arret de la
    simulation, le repositionnement de la voiture et le 
    redémarrage du controller
    Elle return None quand tout va bien et "Restart" lorsqu'elle
    restart la simulation.
    """
    INITIAL_trans = [3.38584, 0.0553475, 0.604829]
    INITIAL_rot=[-0.102639, -0.991788, -0.0763015 ,0.18082]
    if np.array([x.getValue() for x in TS]).any()==1:
        trans_field.setSFVec3f(INITIAL_trans)
        rot_field.setSFRotation(INITIAL_rot)
        robot_node.resetPhysics()
        driver.simulationReset()
        robot_node.restartController()
        print("Restart")
        return
    return
    
