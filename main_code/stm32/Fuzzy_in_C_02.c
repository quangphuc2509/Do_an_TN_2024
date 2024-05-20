#include <stdio.h>
#include <stdint.h>

float triaf(float x, float A[3])
{
    float Ket_qua;
    float Temp_1;
    
    // Ve phuong trinh duong thang trong 2 mien a->b vs b->c
    if(x >= A[0] && x < A[1])
    {
        Temp_1 = 1.0 - (1.0/(A[1]-A[0]))*A[1];  // he so b trong y = ax+b
        Ket_qua = ((1.0/(A[1] - A[0]))*x) + Temp_1;
    }
    else if (x >= A[1] && x <= A[2])
    {
        Temp_1 = 1 - (-1/(A[2]-A[1]))*A[1];
        Ket_qua = ((-1/(A[2]-A[1]))*x) + Temp_1;
    }
    else
    {
        //printf("Khong thuoc tap hop");
        Ket_qua = 0;
    }    
    return Ket_qua;
}

// Collum = 1, Row = 0
int Kiem_tra(float x, int8_t Collum_Row, float Input[3][3], int8_t Rule[3][3])
{
    int i = 0, j = 0;
        //Kiem tra x co thuoc tap hop Input nao
        for(i = 0; i<3; i++)
        {
            if(x >= Input[i][0] && x <= Input[i][2])
            {
                printf("%f thuoc tap hop D %d \n",x, i);

                if(Collum_Row == 1)  // Neu la cot thi tat ca cot cua vi tri ma x thuoc thi rule se bang 1
                {
                    for(j=0; j<3; j++)
                    {
                        Rule[i][j] = 1;
                        
                    }
                }
                else if (Collum_Row == 0) // Neu la hang thi tat ca hang cua vi tri ma x thuoc thi rule se bang 1
                {
                    for(j=0; j<3; j++)
                    {
                        Rule[j][i] = 1;
                        
                    }
                }
            }
            else if (x < Input[i][0] || x > Input[i][2])
            {
                if(Collum_Row == 1)  // Neu la cot thi tat ca cot cua vi tri ma x thuoc thi rule se bang 1
                {
                    for(j=0; j<3; j++)
                    {
                        Rule[i][j] = 0;
                        
                    }
                }
                else if (Collum_Row == 0) // Neu la hang thi tat ca hang cua vi tri ma x thuoc thi rule se bang 1
                {
                    for(j=0; j<3; j++)
                    {
                        Rule[j][i] = 0;
                        
                    }
                }
            }
        }
    
    
}

struct Input_01
{
    float Min, Max;
    float (*triaf)(float, float, float, float);
};

int main()
{
    // Bien dem
    int i, j, k;

    float x1 = 0.2; // An x
    float D1[3][3], D2[3][3];
    float M[3];
    float Tong[10];

    // Input Mang Bs
    float B1[3] = {0, 2, 5};
    float B2[3] = {0, 3, 10};
    float B3[3] = {-1, 2, 4};

    // Input Mang C
    float C1[3] = {-2, 2, 5};
    float C2[3] = {1, 3, 15};
    float C3[3] = {-1, 1, 4};

    // Rule
    int8_t Rule_01[3][3], Rule_02[3][3];
    int8_t Rule_X[3][3];

    // Output
    float Output[3] = {0, 50, 100};

    // Ma tran out put cho luat theo input
    float Matrix_Rule[3][3] = {{0, 0, 1}, {0, 1, 2}, {1, 2, 2}};


    // Gan Input lai vao Mang D1 vs D2
    for (i = 0; i<3; i++)
    {
        // Tao ra mang Input 1 vao D1 
        // Input dau tien quy dinh theo *cot
        D1[0][i] = B1[i];
        D1[1][i] = B2[i]; 
        D1[2][i] = B3[i];

        // Tao ra mang Input 2 vao D2
        // Input dau tien quy dinh theo *hang
        D2[0][i] = C1[i];
        D2[1][i] = C2[i]; 
        D2[2][i] = C3[i];
    }

    // Tao Rule
    Kiem_tra(x1, 1, D1, Rule_01);
    Kiem_tra(x1, 0, D2, Rule_02);

    // Tim Rule
    // Nhan tich chap 2 Rule 01 vs Rule_02 de tim diem giao nhau
    for(i = 0 ; i<3; i++)
    {
        for(j = 0 ; j<3; j++)
        {
            Rule_X[i][j] = Rule_01[i][j] * Rule_02[i][j];
        }
    }

    // Khoi tao mmang de chua gia tri de so sanh
    float SS1, SS2;
    float Rule_SS[3][3]; // bien luu gia tri so sanh
    // So sanh theo luat Min-Max
    for(i = 0 ; i<3; i++)
    {
        for(j = 0 ; j<3; j++)
        {
            if(Rule_X[i][j] == 1)
            {
                SS1 = triaf(x1, D1[i]);
                SS2 = triaf(x1, D2[j]);
                if(SS1 < SS2)
                {
                    printf("001 \n");
                    Rule_SS[i][j] = SS1;
                    printf("%f\n", Rule_SS[i][j]);
                }
                else
                {
                    printf("002 \n");
                    Rule_SS[i][j] = SS2;
                    printf("%f\n", Rule_SS[i][j]);
                }
            }
            else
            {
                Rule_SS[i][j] = 0;
            }
        }
    }

    // Xu li Rule
    for(j = 0 ; j<3; j++)
    {
        printf("\n");
        for(i = 0 ; i<3; i++)
        {
            if(Matrix_Rule[i][j] == 1)
            {
                for(k=0; k<3; k++)
                {
                    if(Matrix_Rule[i][j] == k)
                    {
                        Tong[0] = Tong[0] + Rule_SS[i][j]*Output[k];
                    }
                }
                
            }
            printf("%d ", Rule_X[i][j]);
        }
    }
    
    printf("Tong tat ca la: %f ", Tong[0] );

    // printf("1");
    // // print de kiem tra
    // for(j = 0 ; j<3; j++)
    // {
    //     printf("\n");
    //     for(i = 0 ; i<3; i++)
    //     {
    //         printf("%d ", Rule_X[i][j]);
    //     }
    // }

    printf("2");
    // print de kiem tra
    for(j = 0 ; j<3; j++)
    {
        printf("\n");
        for(i = 0 ; i<3; i++)
        {
            printf("%f ", Rule_SS[i][j]);
        }
    }



    
    printf("\n");
    // Tinh ra gia tri cua Input
    for(i = 0 ; i<3; i++)
    {
        M[i] = triaf(x1, D2[i]);
        printf("Gia tri M%d la %f \n", i, M[i]);
    }

    //printf("Ket qua la: %2f", C); 

    return 0;
}