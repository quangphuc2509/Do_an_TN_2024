/*
 * PID_Control.h
 *
 *  Created on: Apr 27, 2024
 *      Author: quang
 */
#include "stm32f4xx_hal.h"
#ifndef INC_PID_CONTROL_H_
#define INC_PID_CONTROL_H_
#include "stdint.h"
#include "math.h"
#include "stdlib.h"


struct Para_Motor{
	float HIGH, LOW;				// Giới hạn động cơ
	float Kp, Ki, Kd, Kb;				// hệ số PID
	float Up, Up_1;					// Thông số khâu P
	double Ui, Ui_1, Ui_Antiwindup;	// Thông số khâu I
	float Ud, Ud_1;					// Thông số khâu D
	double ek, ek_1;				// Sai số tốc độ động cơ
	double Temp_PWM;
	uint16_t Out_PWM;				// Giá trị PWM điều khiển động
	float Out_fPWM;
	uint32_t Encoder, Encoder_P;	// Giá trị đọc encoder động cơ
	float RPM_Avg, RPM, Temp[20], SP_RPM;	// Tốc độ động cơ

};

extern uint16_t PPR;	// Pulse per round
extern float Time_Interrupt;
extern float GT_Convert_radian;
extern uint16_t HIGH_Limit_PWM;
extern uint16_t LOW_Limit_PWM;
extern int32_t delta;

float Average_5_times(float Var, float Temp[20]);
void read_encoder(TIM_HandleTypeDef* htim, struct Para_Motor* pt_Para_M);
void RPM_Calc(TIM_HandleTypeDef* htim, struct Para_Motor* pt_Para_M );
float Anti_Windup(float Out_PWM, uint16_t HIGH_Limit, uint16_t LOW_Limit, float Kb);
void PID_control(TIM_HandleTypeDef* htim,struct Para_Motor* pt_Para_M, uint32_t channel);


#endif /* INC_PID_CONTROL_H_ */
