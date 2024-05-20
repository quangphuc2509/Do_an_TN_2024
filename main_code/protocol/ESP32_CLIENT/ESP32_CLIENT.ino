#include <WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>

const char* ssid = "Teacher";
const char* password = "123456@xX";
const char* host = "10.0.60.89";
const uint16_t port = 55555;

int bitArray_int[5];

String RxData[6];
String first32Bits[6];
String remainingBits[6];
String binaryString;
String  receivedData;

void setup() 
{
  Wire.begin(); // Khởi động thư viện Wire (I2C)
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) 
    {
      delay(500);
      Serial.print(".");
    }
  Serial.println("WiFi connected");
}


void loop() 
{

  WiFiClient client;
  if (!client.connect(host, port)) 
    {
      return;     
    }
 
  while (client.connected()) 
    {

      Wire.beginTransmission(0x12);
     
      if (client.available()) 
      {
        

          receivedData= client.readStringUntil('\n');
          Serial.print("Received data from server: ");
          Serial.println(receivedData);
          int index = 0;
          for (int i = 0; i < 6; i++) 
          {
                // Trích xuất 32 bit từ chuỗi nhận được
                String elementString = receivedData.substring(index, index + 40);
                
                // Lưu phần tử vào mảng RxData
                RxData[i] = elementString;

                // Di chuyển chỉ mục tới 32 bit kế tiếp
                index += 40;
          }
        
          for (int i = 0; i < 6; i++) 
          {
            // Tách thành 32 bit liên tiếp và phần còn lại
            first32Bits[i] = RxData[i].substring(0, 32);
            remainingBits[i] = RxData[i].substring(32);

            // In ra 24 bit đầu tiên và phần còn lại
            Serial.print("First 32 bits: ");
            Serial.println(first32Bits[i]);
            Serial.print("Remaining bits: ");
            Serial.println(remainingBits[i]);
            receivedData.remove(0);

               // Bắt đầu gửi dữ liệu tới địa chỉ I2C    ////////////////////////////////////////////////////////////
            for (int j = 0; j < 5; j++) 
            {
                
                if (j < 4) {
                    binaryString = first32Bits[i].substring(j * 8, (j + 1) * 8);
                } else {
                    binaryString = first32Bits[i].substring(j * 8) + remainingBits[i];
                }
                
                // Chuyển đổi từ chuỗi nhị phân thành số nguyên và gán vào mảng
                bitArray_int[j] = strtol(binaryString.c_str(), NULL, 2);
                           
                Wire.write(bitArray_int[j]); // Gửi dữ liệu   ////////////////////////////////////////////////////////////////////////////////    
                            
            }
            
          
            // receivedData.remove(0);
            // memset(first32Bits, 0, sizeof(first32Bits));
            // memset(remainingBits, 0, sizeof(remainingBits));
            // binaryString.remove(0);
            // memset(bitArray_int, 0, sizeof(bitArray_int));
          
          }
       
      
      }// ifclient.available



       Wire.endTransmission();

    // Kết thúc gửi dữ liệu  ///////////////////////////////////////////////////////////////////////////////////
    }//while client.connect
      

  client.stop();

}


