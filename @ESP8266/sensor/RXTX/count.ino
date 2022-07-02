#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>

// WiFi
const char *ssid = "DIRECT-AIRVA"; // Enter your WiFi name
const char *password = "ABCDEFGH4321";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "airva.local";
const char *topic = "airva/device/#";
const char *pub_topic = "airva/device/esp8266_occupantscounter0x01/occupants";
const char *mqtt_username = "mqttadmin";
const char *mqtt_password = "over224433";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600); // Esp

  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi.");
    delay(500);
  }
  
  Serial.println("Connected to the WiFi network");
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Public emqx mqtt broker connected");
      Serial.println("MQTT Ready.");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      Serial.println("Error..");
      delay(2000);
    }
  }
  
  client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {

  if ( strcmp(topic, "airva/device/esp8266node1") == 0 ) {
    Serial.print("READY........");

    StaticJsonBuffer<200> JSONBuffer;
    char JSONinData[150];
    Serial.print("Callback From- ");
    Serial.println(topic);

    Serial.print("payload: ");
    for (int i = 0; i < length; i++) {
      JSONinData[i] = (char)payload[i];
    }
    Serial.println();

    JsonObject& parsed = JSONBuffer.parseObject(JSONinData);
    if (!parsed.success()) {   //Check for errors in parsing
      Serial.println("Parsing failed");
      delay(2000);
      return;
    }
    
  }
}

int occupants = 0;
int max_occupants = 100;
int min_occupants = 0;
int inByte = 0;

void loop() {
  client.loop();
  
  while(Serial.available()) {
    
    inByte = Serial.read();
    if( inByte == 'i' && occupants < max_occupants )
      occupants++;
    else if( inByte == 'o' && occupants > min_occupants )
      occupants--;
    
    Serial.println(occupants);
    String payload = String(occupants);
    char attributes[3];
    payload.toCharArray(attributes, 3);
    
    client.publish(pub_topic, attributes);
  }
}