#include <CoVAPSy_Lidar.h>
#include "tim.h"
#include "stdint.h"
#include "usart.h"

// Initialisation du Lidar SLAMTECH A2M12
void Lidar_init(void) {
	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2); //Lidar
	HAL_Delay(100);
	__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, 300); 			//démarrage du lidar par PWM
	HAL_Delay(2000);
	uint8_t packet_CMD_RESET_SCAN[2] = { 0xA5, 0x25 };
	uint8_t packet_CMD_START_SCAN[2] = { 0xA5, 0x20 };
	HAL_UART_Transmit(&huart1, packet_CMD_RESET_SCAN, 2, 100);	// Reset LiDAR
	HAL_Delay(15);
	HAL_UART_Transmit(&huart1, packet_CMD_START_SCAN, 2, 100);	// Start LiDAR
}


