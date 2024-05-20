#include "WiFi.h"

const char* ssid = "Teacher";
const char* password =  "123456@xX";

const uint16_t port = 55555;
const char * host = "10.0.62.48";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;
  // put your main code here, to run repeatedly:

  if(!client.connect(host, port)) {
    Serial.println("Connecting successful");
    delay(1000);
    return;
  }

  client.println("Hello Im ESP Client");

  delay(1000);

}
