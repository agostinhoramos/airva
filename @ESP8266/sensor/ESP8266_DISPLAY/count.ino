#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// OLED
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


#include <WEMOS_SHT3X.h>
#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel pixels(1, D7, NEO_GRB + NEO_KHZ800);

//0x31
#define OLED_RESET -1
Adafruit_SSD1306 display(OLED_RESET);
SHT3X sht30(0x45);


// WiFi
const char *ssid = "DIRECT-AIRVA"; // Enter your WiFi name
const char *password = "ABCDEFGH4321";  // Enter WiFi password

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
  Serial.begin(9600);
  pixels.begin();

  // OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      writeOLED("Connecting to WiFi.", 1);
      delay(500);
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
          writeOLED("MQTT Ready.", 2);
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          writeOLED("Error..", 2);
          delay(2000);
      }
  }
  // publish and subscribe
  //client.publish(topic, "hello emqx");
  client.subscribe(topic);
}

int occupants = 0;
int semaphore = -1;

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  if( strcmp(topic, "airva/device/esp8266_display0x01/set") == 0 ){
    Serial.print("READY........");

    StaticJsonBuffer<200> JSONBuffer;
    char JSONinData[150];
    Serial.print("Callback From- ");
    Serial.println(topic);

    //String strChar = "";
    for(int i =0; i<length; i++){
      //strChar += (char)payload[i];
      JSONinData[i] = (char)payload[i];
    }
    Serial.println();

    JsonObject& parsed = JSONBuffer.parseObject(JSONinData);  
    if (!parsed.success()) {   //Check for errors in parsing
      Serial.println("Parsing failed");
      delay(2000);
      return;
    }
  
    occupants = parsed["occupants"];//strChar.toInt();
    writeOLED( String(occupants), 3);

    semaphore = parsed["semaphore"];
    if( semaphore >= 0 && semaphore <= 3 ){
      semaphoreLED(semaphore);
    }
    
  }
}

void loop() {
  client.loop();
}

void semaphoreLED(int opt){
    if( opt == 0 ){ // DISABLED
      pixels.setPixelColor(0, pixels.Color(1, 1, 1));
      pixels.show();
    }else
    if( opt == 1 ){ // GREEN
      pixels.setPixelColor(0, pixels.Color(0, 255, 0));
      pixels.show();
    } else
    if( opt == 2 ){ // YELLOW
      pixels.setPixelColor(0, pixels.Color(255, 255, 0));
      pixels.show();
    }else
    if( opt == 3 ){ // RED
      pixels.setPixelColor(0, pixels.Color(255, 0, 0));
      pixels.show();
    }
}

void writeOLED(String string, int s)
{
    display.clearDisplay();
    display.setTextSize(s);
    display.setCursor(0, 0);
    display.setTextColor(WHITE);
    display.println(string);
    display.display();
}