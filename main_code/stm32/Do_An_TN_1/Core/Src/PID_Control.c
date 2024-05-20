/*
 * PID_Control.c
 *
 *  Created on: Apr 27, 2024
 *      Author: quang
 */
#include "PID_Control.h"

uint16_t PPR = 2688;
float Time_Interrupt = 0.005;
float GT_Convert_radian = 0.1047197551;
uint16_t HIGH_Limit_PWM = 999;
uint16_t LOW_Limit_PWM = 0;
int32_t delta = 0;

float Average_5_times(float Var, float Temp[20]){
    float sum = 0, Out_Average_Var; // Initialize sum to 0
    for (int i = 0; i < 19; i++)
    {
        Temp[i] = Temp[i + 1];  // gán giá trị hiện tại vào giá trị trước
        sum += Temp[i];        // Cộng dần các giá trị vừa lưu
    }
    // Gán giá trị mới nhất
    Temp[19] = Var;
    sum += Temp[19] ;
    // Tính trung bình
    Out_Average_Var = sum / 20;

    return Out_Average_Var;
}

void read_encoder(TIM_HandleTypeDef* htim, struct Para_Motor* pt_Para_M){
	pt_Para_M->Encoder = __HAL_TIM_GET_COUNTER(htim);
}

void RPM_Calc(TIM_HandleTypeDef* htim, struct Para_Motor* pt_Para_M ){

	pt_Para_M->Encoder = __HAL_TIM_GET_COUNTER(htim);		// Cập nhật encoder
	delta = abs(pt_Para_M->Encoder - pt_Para_M->Encoder_P);		//Lấy chênh lệch 2 khoảng encoder

	// Kiểm tra giá trị chênh lệch lớn hơn nửa vòng là vô lý nên lấy giá trị tràn trừ giá trị chênh lệch
	if (delta >= __HAL_TIM_GET_AUTORELOAD(htim) / 2){
		delta = __HAL_TIM_GET_AUTORELOAD(htim) - delta;
	}
	pt_Para_M->RPM_Avg = (delta / (PPR*4*Time_Interrupt)*60);
	pt_Para_M->RPM = Average_5_times(pt_Para_M->RPM_Avg, pt_Para_M->Temp);

	pt_Para_M->Encoder_P = pt_Para_M->Encoder;

}

float Anti_Windup(float Out_PWM, uint16_t HIGH_Limit, uint16_t LOW_Limit, float Kb){
    float e_reset = 0;
    float Ui_anti;

    if (Out_PWM > HIGH_Limit){
        e_reset = (HIGH_Limit - Out_PWM );
    }
    else if (Out_PWM < LOW_Limit){
        e_reset = (LOW_Limit - Out_PWM);
    }
    else {
        e_reset = 0;
    }
    Ui_anti = Time_Interrupt * e_reset * Kb;

    return Ui_anti;
}

void PID_control(TIM_HandleTypeDef* htim,struct Para_Motor* pt_Para_M, uint32_t channel){
	pt_Para_M->ek = (pt_Para_M->SP_RPM - pt_Para_M->RPM);	// Xác định sai số

	pt_Para_M->Up = pt_Para_M->Kp * pt_Para_M->ek;			// Xác định Up
	pt_Para_M->Ui = pt_Para_M->Ui_1 + pt_Para_M->Ki * pt_Para_M->ek_1 * Time_Interrupt + pt_Para_M->Ui_Antiwindup;
	pt_Para_M->Ud = pt_Para_M->Ud_1 * (pt_Para_M->ek - pt_Para_M->ek_1);

	// Anti windup
	pt_Para_M->Ui_Antiwindup = Anti_Windup(pt_Para_M->Temp_PWM, HIGH_Limit_PWM, LOW_Limit_PWM, pt_Para_M->Kb);

	pt_Para_M->Temp_PWM = pt_Para_M->Up + pt_Para_M->Ui + pt_Para_M->Ud;

	pt_Para_M->Out_PWM = round(pt_Para_M->Temp_PWM);

	if (pt_Para_M->Out_PWM >= 999){
		pt_Para_M->Out_PWM = 999;
	}
	else if (pt_Para_M->Out_PWM <= 0){
		pt_Para_M->Out_PWM = 0;
	}

	// Gán lại giá trị
	pt_Para_M->ek_1 = pt_Para_M->ek;
	pt_Para_M->Ui_1 = pt_Para_M->Ui;
	pt_Para_M->Ud_1 = pt_Para_M->Ud_1;



	__HAL_TIM_SET_COMPARE(htim, channel, pt_Para_M->Out_PWM);
}



