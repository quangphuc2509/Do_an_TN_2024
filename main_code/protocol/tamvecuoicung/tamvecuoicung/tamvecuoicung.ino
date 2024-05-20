#include <WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>


const char* ssid = "Teacher";
const char* password = "123456@xX";
const char* host = "10.0.60.89";
const uint16_t port = 55555;

int bitArray_int[5];
uint count =0;
String binaryString;
String receivedData;
String first32Bits;
String remainingBits;
void setup() 
{
  Wire.begin(); // Khởi động thư viện Wire (I2C)
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) 
    {
      Serial.print(".");
    }
  Serial.println("WiFi connected");
}



void loop() {
    WiFiClient client;
    while (!client.connect(host, port)) {
        Serial.println("Connection to server failed. Retrying...");
        delay(1000); // Chờ 1 giây trước khi thử kết nối lại
    }
count = 0;
    while (client.connected()) {
        // Đọc dữ liệu từ client vào biến receivedData
        String receivedData = client.readString();

        // Xử lý dữ liệu theo từng phần 40 ký tự
        int startIndex = 0;
        while (startIndex + 40 <= receivedData.length()) {
            String packet = receivedData.substring(startIndex, startIndex + 40);
            
        count+=1;
        // Tách thành 32 bit liên tiếp và phần còn lại
        first32Bits = packet.substring(0, 32);
        remainingBits = packet.substring(32, 40);

        Serial.print("Da nhan la thu: ");
        Serial.println(count);

        // Thiết lập và gửi dữ liệu qua I2C
        Wire.beginTransmission(0x12);
        for (int i = 0; i < 5; i++) {
            if (i < 4) {
                binaryString = first32Bits.substring(i * 8, (i + 1) * 8);
            } else {
                binaryString = first32Bits.substring(i * 8) + remainingBits;
            }
            bitArray_int[i] = strtol(binaryString.c_str(), NULL, 2);
            Wire.write(bitArray_int[i]);
        }
        Wire.endTransmission();
            startIndex += 40;
        }
    }

    client.stop(); // Đóng kết nối
}
