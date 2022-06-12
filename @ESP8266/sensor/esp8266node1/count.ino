#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// OLED
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
//0x31
#define OLED_RESET -1
Adafruit_SSD1306 display(OLED_RESET);


// WiFi
const char *ssid = "CASA RAMOS"; // Enter your WiFi name
const char *password = "ngueTela";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "airva.local";
const char *topic = "airva/device/#";
const char *mqtt_username = "mqttadmin";
const char *mqtt_password = "over224433";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // Set software serial baud to 115200;
  Serial.begin(115200);

  // OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  writeOLED("0");
  
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  
  while (!client.connected()) {
      String client_id = "esp8266-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
      if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
          Serial.println("Public emqx mqtt broker connected");
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }
  // publish and subscribe
  //client.publish(topic, "hello emqx");
  client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  if( strcmp(topic, "airva/device/esp8266node1/oledcountrgb") == 0 ){
    Serial.print("READY........");

    StaticJsonBuffer<200> JSONBuffer;
    char JSONinData[150];
    Serial.print("Callback From- ");
    Serial.println(topic);


    Serial.print("data:");  
    Serial.print("payload: ");
    for(int i =0; i<length; i++){
      Serial.print((char)payload[i]);
      JSONinData[i] = (char)payload[i];
    }
    Serial.println();
    
    
    JsonObject& parsed = JSONBuffer.parseObject(JSONinData);  
    if (!parsed.success()) {   //Check for errors in parsing
      Serial.println("Parsing failed");
      delay(2000);
      return;
    }
  
    long count_detect = parsed["count_detect"];
    Serial.println("Parsed Data:");
    Serial.println(count_detect);
    writeOLED( String(count_detect) );
  }
  
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void loop() {
  client.loop();
}

void writeOLED(String string)
{
    display.clearDisplay();
    display.setTextSize(3);
    display.setCursor(0, 0);
    display.setTextColor(WHITE);
    display.println(string);
    display.display();

}
