
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

int estado_co2=0;
int recebido_co2=0;
int ppm_co2=-1;
int ppm_co2_tmp=0;

// WiFi
const char *ssid = "DIRECT-AIRVA"; // Enter your WiFi name
const char *password = "ABCDEFGH4321";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "airva.local";
const char *topic = "airva/device/#";
const char *pub_topic = "airva/device/esp8266co2";
const char *mqtt_username = "mqttadmin";
const char *mqtt_password = "over224433";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
  // Set software serial baud to 115200;
  Serial.begin(19200);

 

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

  //  client.publish(pub_topic, jsonmain);

  client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  if ( strcmp(topic, "airva/device/esp8266co2") == 0 ) {
    Serial.print("READY........");

    StaticJsonBuffer<200> JSONBuffer;
    char JSONinData[150];
    Serial.print("Callback From- ");
    Serial.println(topic);


    Serial.print("data:");
    Serial.print("payload: ");
    for (int i = 0; i < length; i++) {
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
  leco2();
  String payloadout = "{";
  payloadout += "\"ppm_co2\":";
  payloadout += ppm_co2;
  payloadout += ", \"detect_co2\":";
  payloadout += recebido_co2;
  payloadout += "}";
  char attributes[3000];
  payloadout.toCharArray(attributes, 3000);

  client.publish(pub_topic, attributes);
}

void leco2()
{
    //porta serie 1 interior
    //FF;FE;02;02;03
    Serial.write(0xFF);  
    delay(10);
    Serial.write(0xFE);
    delay(10);
    Serial.write(0x02);
    delay(10);
    Serial.write(0x02);
    delay(10);
    Serial.write(0x03);
    delay(1000);
         
    //do interior
    while(Serial.available())
    {
        recebido_co2=Serial.read();
        //Serial.println(recebido_co2);
        if(recebido_co2==255 && estado_co2==0)
        {
            estado_co2++;
        }
        else if(recebido_co2==250 && estado_co2==1)
        {
            estado_co2++;
        }
        else if(recebido_co2==2 && estado_co2==2)
        {
            estado_co2++;
        }
        else if(estado_co2==3)
        {
            ppm_co2_tmp= recebido_co2*255;
            estado_co2++;
        }
        else if(estado_co2==4)
        {
            ppm_co2_tmp+= recebido_co2;
            estado_co2=0;
            ppm_co2=ppm_co2_tmp;
        }
        else
        {
            estado_co2=0;
        }
    }
}
