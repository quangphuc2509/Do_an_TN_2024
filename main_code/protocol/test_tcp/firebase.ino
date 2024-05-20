#include <WiFi.h>
#include <FirebaseESP32.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include "DHT.h"
#include <BH1750.h>
#include <Wire.h>

#define WIFI_SSID "Q coffee_tea"                //"Van Toan"  //"Q coffee_tea"               //"Hieu_2.4G"
#define WIFI_PASSWORD "250ahoangdieu2"            //"123456789"//"250ahoangdieu2"          //"13061969"
#define API_KEY "AIzaSyD3ukZCnuW3VTmmWARckRhJ6CgtgqTNkv8"

#define DATABASE_URL "https://fir-doan-67307-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define USER_EMAIL "atkute158@gmail.com"
#define USER_PASSWORD "vantrung"

#define DHTPIN 4
#define DHTTYPE DHT22

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter(0x23);
float final=0;

void setup()
{

  Serial.begin(115200);
  dht.begin();
  Wire.begin();
  lightMeter.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  config.token_status_callback = tokenStatusCallback;
  Firebase.reconnectNetwork(true);
  fbdo.setBSSLBufferSize(4096, 1024);
  Firebase.begin(&config, &auth);
  Firebase.setDoubleDigits(5);

}
void sendDatatoServer(float temp, float humi, float tilemua)
{
  if (Firebase.ready()) 
  {
    Firebase.setFloat(fbdo, "Temp", temp);
    Firebase.setFloat(fbdo, "Humidity", humi);
    Firebase.setFloat(fbdo, "Tilemua", tilemua);
    if (Firebase.getFloat(fbdo, "/Get")) 
  {
    final = fbdo.to<float>();
  }
  }
}

void hoatdong(float TilemuaTonghop, float anhsang)
{
    if (TilemuaTonghop < 85)
      Serial.println("Close");
    else
      Serial.println("Activate");
}

float tinhtilemua(float temp, float humidity)
{
  float tile,DeEsat,Esat,Tw,DentaT,To,DentaS;
  float z = 0.019;
  float a = (17.27*temp)/(temp+237.3);
  DeEsat = (1464.36*exp(a))/pow((temp+237.3),2);
  float b = 17.27*temp/(temp+237.3);
  Esat = 6.1078*exp(b);
  Tw = temp-(Esat*(1-humidity))/(0.000643*1013+DeEsat);
  DentaT = 0.215-0.099*humidity+1.018*pow(humidity,2);
  To = -5.87-0.1042*z+0.0885*pow(z,2)+16.06*humidity-9.614*pow(humidity,2);
  DentaS = 2.374-1.634*humidity;
  float c = (temp/10 - DentaT - To)/DentaS;
  tile = (1/(1+exp(c)))*100;
  return tile;
}
void loop()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  uint16_t lux = lightMeter.readLightLevel();
  float tilemua = tinhtilemua(t,(h/100));
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  
  Serial.print(F("TiLeMua: "));
  Serial.print(tilemua);
  Serial.print(F("% "));
  
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  sendDatatoServer(t,h,tilemua);
  Serial.print("TilemuaTonghop: ");
  Serial.print(final, 2);
  Serial.print(F("% "));
  hoatdong(final,lux);

  delay(10000);
}