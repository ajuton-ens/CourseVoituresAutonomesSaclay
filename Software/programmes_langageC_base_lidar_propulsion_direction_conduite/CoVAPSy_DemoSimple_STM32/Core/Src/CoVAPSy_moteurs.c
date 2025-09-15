/*
 * CoVAPSy_moteurs.c
 *
 *  Created on: May 21, 2023
 *      Author: ajuton
 */
#include "CoVAPSy_moteurs.h"

void Propulsion_init(void){
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
}

void Direction_init(void){
	HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_4);
}

void set_direction_degres(float angle_degre)
{
	uint32_t largeur_impulsion_us;
	if (angle_degre < -DIR_ANGLE_MAX)
		angle_degre = -DIR_ANGLE_MAX;
	else if (angle_degre > DIR_ANGLE_MAX)
		angle_degre = +DIR_ANGLE_MAX;
	largeur_impulsion_us = DIR_MILIEU - (DIR_BUTEE_GAUCHE - DIR_BUTEE_DROITE)*angle_degre/(2*DIR_ANGLE_MAX);
	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_4, largeur_impulsion_us);

}

void set_vitesse_m_s(float vitesse_m_s){
	uint32_t largeur_impulsion_us;
	if (vitesse_m_s == 0)
	{
		largeur_impulsion_us = PROP_REPOS ;
	}
	else if (vitesse_m_s < 0){
		if(vitesse_m_s < -V_MAX_HARD)
			vitesse_m_s  = -V_MAX_HARD;
		largeur_impulsion_us = PROP_POINT_MORT_NEG + (PROP_MAX - PROP_POINT_MORT) * vitesse_m_s / V_MAX_HARD;
		//version variateur bizarre
		//largeur_impulsion_us = PROP_POINT_MORT - (PROP_MAX - PROP_POINT_MORT) * vitesse_m_s / V_MAX_HARD;
	}
	else if (vitesse_m_s > 0){
		if (vitesse_m_s > V_MAX_SOFT)
			vitesse_m_s = V_MAX_SOFT;
		largeur_impulsion_us = PROP_POINT_MORT + (PROP_MAX - PROP_POINT_MORT) * vitesse_m_s / V_MAX_HARD;
		//version variateur bizarre
		//largeur_impulsion_us = PROP_POINT_MORT_NEG - (PROP_MAX - PROP_POINT_MORT) * vitesse_m_s / V_MAX_HARD;
	}
	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, largeur_impulsion_us);
}

void recule(void){
    set_vitesse_m_s(-V_MAX_HARD);
    HAL_Delay(200);
    set_vitesse_m_s(0);
    HAL_Delay(100);
    set_vitesse_m_s(-4);
}
