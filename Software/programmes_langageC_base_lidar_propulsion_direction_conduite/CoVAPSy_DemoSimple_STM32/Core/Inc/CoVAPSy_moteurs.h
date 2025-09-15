/*
 * CoVAPSy_moteurs.h
 *
 *  Created on: May 21, 2023
 *      Author: ajuton
 */
#include "tim.h"
#include <stdint.h>

#ifndef INC_COVAPSY_MOTEURS_H_
#define INC_COVAPSY_MOTEURS_H_

//constantes propulsion
#define V_MAX_SOFT 2.0
#define V_MAX_HARD 8.0
#define PROP_REPOS 1500
#define PROP_POINT_MORT 1440
#define PROP_POINT_MORT_NEG 1560
#define PROP_MAX 1250

//constantes direction
#define DIR_ANGLE_MAX 18.0
#define DIR_BUTEE_DROITE 900
#define DIR_BUTEE_GAUCHE 1300
#define DIR_MILIEU 1100

void Propulsion_init(void);
void Direction_init(void);
void set_direction_degres(float angle_degre);
void set_vitesse_m_s(float vitesse_m_s);
void recule(void);

#endif /* INC_COVAPSY_MOTEURS_H_ */
