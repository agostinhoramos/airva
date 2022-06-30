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
const char *pub_topic = "airva/device/esp8266node3/count";
const char *mqtt_username = "mqttadmin";
const char *mqtt_password = "over224433";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

void setup() {
  Serial.begin(9600); // Esp
  Serial1.begin(9600); // Arduino


  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi.");
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
      Serial.println("MQTT Ready.");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      Serial.println("Error..");
      delay(2000);
    }
  }
  // publish and subscribe
  client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {
  /* Serial.print("Message arrived in topic: ");
    Serial.println(topic);*/

  if ( strcmp(topic, "airva/device/esp8266node1/count/") == 0 ) {
    Serial.print("READY........");

    StaticJsonBuffer<200> JSONBuffer;
    char JSONinData[150];
    Serial.print("Callback From- ");
    Serial.println(topic);


    Serial.print("data:");
    Serial.print("payload: ");
    for (int i = 0; i < length; i++) {
      //Serial.print((char)payload[i]);
      JSONinData[i] = (char)payload[i];
    }
    Serial.println();


    JsonObject& parsed = JSONBuffer.parseObject(JSONinData);
    if (!parsed.success()) {   //Check for errors in parsing
      Serial.println("Parsing failed");
      delay(2000);
      return;
    }

    //long count_detect = parsed["count_detect"];
    //Serial.println("Parsed Data:");
    //Serial.println(count_detect);
  }

  /*Serial.print("Message:");
    for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");*/
}

int changed = 0;
int inByte;
char *payload;

void loop() {
  client.loop();
  
  if(Serial1.available()) {
    while(Serial1.available() > 0){
      inByte = Serial1.read();
     // payload = inByte;
    }
  }
  Serial.print("Envia");
  char my = char(inByte);
  Serial.println(my);
    
  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    //Serial.println( inputString );
    client.publish(pub_topic, payload);
  }


}
