/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define RUN_LIGHT_Pin GPIO_PIN_2
#define RUN_LIGHT_GPIO_Port GPIOE
#define STOP_LIGHT_Pin GPIO_PIN_3
#define STOP_LIGHT_GPIO_Port GPIOE
#define WARNING_LIGHT_Pin GPIO_PIN_4
#define WARNING_LIGHT_GPIO_Port GPIOE
#define PULSE_STEPPER_Pin GPIO_PIN_0
#define PULSE_STEPPER_GPIO_Port GPIOA
#define TX_HC05_Pin GPIO_PIN_2
#define TX_HC05_GPIO_Port GPIOA
#define RX_HC05_Pin GPIO_PIN_3
#define RX_HC05_GPIO_Port GPIOA
#define PWM_R_Pin GPIO_PIN_5
#define PWM_R_GPIO_Port GPIOA
#define ENCODER_R1_Pin GPIO_PIN_6
#define ENCODER_R1_GPIO_Port GPIOA
#define ENCODER_R2_Pin GPIO_PIN_7
#define ENCODER_R2_GPIO_Port GPIOA
#define PWM_L_Pin GPIO_PIN_9
#define PWM_L_GPIO_Port GPIOE
#define SCL_LCD_Pin GPIO_PIN_10
#define SCL_LCD_GPIO_Port GPIOB
#define SDA_LCD_Pin GPIO_PIN_11
#define SDA_LCD_GPIO_Port GPIOB
#define ENCODER_L1_Pin GPIO_PIN_12
#define ENCODER_L1_GPIO_Port GPIOD
#define ENCODER_L2_Pin GPIO_PIN_13
#define ENCODER_L2_GPIO_Port GPIOD
#define TX_ESP32_Pin GPIO_PIN_9
#define TX_ESP32_GPIO_Port GPIOA
#define RX_ESP32_Pin GPIO_PIN_10
#define RX_ESP32_GPIO_Port GPIOA
#define USER_BUTTON_Pin GPIO_PIN_0
#define USER_BUTTON_GPIO_Port GPIOD
#define STOP_Button_Pin GPIO_PIN_1
#define STOP_Button_GPIO_Port GPIOD
#define START_Button_Pin GPIO_PIN_2
#define START_Button_GPIO_Port GPIOD
#define DIR_L_Pin GPIO_PIN_5
#define DIR_L_GPIO_Port GPIOD
#define DIR_R_Pin GPIO_PIN_6
#define DIR_R_GPIO_Port GPIOD
#define DIR_SERVO_Pin GPIO_PIN_7
#define DIR_SERVO_GPIO_Port GPIOD
#define SCK_MAX7219_Pin GPIO_PIN_3
#define SCK_MAX7219_GPIO_Port GPIOB
#define MISO_MAX7129_Pin GPIO_PIN_4
#define MISO_MAX7129_GPIO_Port GPIOB
#define MOSI_MAX7129_Pin GPIO_PIN_5
#define MOSI_MAX7129_GPIO_Port GPIOB
#define ESP32_SCL_Pin GPIO_PIN_6
#define ESP32_SCL_GPIO_Port GPIOB
#define ESP32_SDA_Pin GPIO_PIN_7
#define ESP32_SDA_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
