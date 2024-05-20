#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include "time.h"

#define DHTPIN 4
#define DHTTYPE DHT22

const char* ssid = "Van Toan";
const char* password = "123456789";

char* mqtt_server = "mqtt-dashboard.com";
int mqtt_port = 1883;



DHT dht(DHTPIN, DHTTYPE);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);


void setupMQTT(){
  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(callback);
}



void reconnect() {
  Serial.print("Attempting MQTT connection...");
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT reconnection...");
    String clientID =  "ESP32Client-";
    clientID += String(random(0xffff),HEX);
    if (mqttClient.connect(clientID.c_str())) {
      Serial.println("connected");
      mqttClient.subscribe("esp32/message: ");
    }
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println("");
  Serial.println("Connected Wifi");
  dht.begin();
  setupMQTT();
}

void loop() {

  if (!mqttClient.connected()) {
    reconnect();
  }
  double h = dht.readHumidity();
  double t = dht.readTemperature();
  double f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  char TempString[8];
  dtostrf(t, 1, 2, TempString);
  Serial.print("Temp: ");
  Serial.println(t);
  //mqttClient.publish("esp32/temp", TempString);

  char HumiString[8];
  dtostrf(h, 1, 2, HumiString);
  Serial.print("Humi: ");
  Serial.println(h);
  char DHT[100];
  strcpy(DHT, TempString);
  strcat(DHT, ",");
  strcat(DHT, HumiString);
  mqttClient.publish("esp32/hum", DHT);
  //mqttClient.publish("esp32/hum", TempString);

  delay(5000);
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("---new message form broken---");
  Serial.print("message: ");
  for (int i=0; i<length; i++){
    Serial.print((char)message[i]);
  }
}