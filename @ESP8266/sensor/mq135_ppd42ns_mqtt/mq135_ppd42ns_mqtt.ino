#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h> 


//MQ-135
#define anInput     A0                        //analog feed from MQ135
#define digTrigger  D2                        //digital feed from MQ135
#define co2Zero     55                        //calibrated CO2 0 level
String gasDetectMq135;


//DSM501
byte buff[2];
int pinPPD42NS = D4;//DSM501A input D8
unsigned long duration;
unsigned long starttime;
unsigned long endtime;
unsigned long sampletime_ms = 1000;
unsigned long lowpulseoccupancy = 0;

unsigned long elapsedtime = 0;
unsigned long timestamp = 0;

float ratio = 0;
float concentration = 0;
int i = 0;
// WiFi
const char *ssid = "DIRECT-AIRVA"; // Enter your WiFi name
const char *password = "ABCDEFGH4321";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "airva.local";
const char *topic = "airva/device/#";
const char *pub_topic = "airva/device/esp8266mq123pp42ns";
const char *mqtt_username = "mqttadmin";
const char *mqtt_password = "over224433";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient); 

void setup() {
  // Set software serial baud to 115200;
  Serial.begin(115200 );

  //MQ-135
  pinMode(anInput, INPUT);                    //MQ135 analog feed set for input
  pinMode(digTrigger, INPUT);                 //MQ135 digital feed set for input

  //pinPPD42NS
  pinMode(pinPPD42NS, INPUT);
  starttime = millis();//get the current time;

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

  if ( strcmp(topic, "/airva/device/esp8266mq123pp42ns") == 0 ) {
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

  //MQ-135
  client.loop();
  int co2now[10];                               //int array for co2 readings
  int co2raw = 0;                               //int for raw value of co2
  int co2comp = 0;                              //int for compensated co2
  int co2ppm = 0;                               //int for calculated ppm
  int zzz = 0;                                  //int for averaging
  int grafX = 0;                                //int for x value of graph
  int value = analogRead(A0);
  int R0 = 176;
  int R2 = 1000;
  float RS;
  float PPM_acetone;

  for (int x = 0; x < 10; x++) {              //samplpe co2 10x over 2 seconds
    co2now[x] = analogRead(anInput);
    delay(200);
  }
  for (int x = 0; x < 10; x++) {                //add samples together
    zzz = zzz + co2now[x];

  }
  co2raw = zzz / 10;                          //divide samples by 10
  co2comp = co2raw - co2Zero;                 //get compensated value
  co2ppm = map(co2comp, 0, 1023, 400, 5000);  //map value for atmospheric levels
  bool stateDetect = digitalRead(digTrigger);

  // convert to voltage:
  float volts = value * 5;
  volts = volts / 1023;
  // calculate RS
  RS = R2 * (1 - volts);
  RS = RS / volts;
  // calculate acetone PPM
  PPM_acetone = 159.6 - 133.33 * (RS / R0);
  // print out the acetone concentration:
  //Serial.println(PPM_acetone);
  // concentração de acetona:
  /*if(stateDetect == HIGH){
    Serial.println("not gas detected = 1");
    }else{
    Serial.println("gas detected = 0");
    }*/
  /***PPD42NS***/

  duration = duration + pulseIn(pinPPD42NS, LOW); //pulseIn(pinPPD42NS, LOW);
  lowpulseoccupancy = lowpulseoccupancy + duration;
  endtime = millis();
  elapsedtime=millis()-starttime;
  
  if ((millis() - starttime) > sampletime_ms) //if the sampel time = = 30s
  {
    ratio =  lowpulseoccupancy / (sampletime_ms * 10.0); //duration/(elapsedtime*10.0); //(lowpulseoccupancy - endtime + starttime + sampletime_ms) / (sampletime_ms * 10.0); // Integer percentage 0=>100
    concentration = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62; // using spec sheet curve
    timestamp=millis()/1000;
    lowpulseoccupancy = 0;
    duration = 0;
    starttime = millis();
  }

   

  String payloadout = "{"; 
  payloadout += "\"mq135\":";
  payloadout += "{";
  payloadout += "\"co2ppm\":";
  payloadout += co2ppm;
  payloadout += ", \"statedetect\":";
  payloadout += stateDetect;
  payloadout += ", \"raw\":";
  payloadout += value;
  payloadout += ", \"ppm_acetone\":";
  payloadout += PPM_acetone;
  payloadout += "}";

  payloadout += ", \"ppd42ns\":";
  payloadout += "{";
  payloadout += "\"lowpulseoccupancy\":";
  payloadout += lowpulseoccupancy;
  payloadout += ", \"ratio\":";
  payloadout += ratio;
  payloadout += ", \"concentration\":";
  payloadout += concentration;
  payloadout += ", \"timestamp\":";
  payloadout += timestamp;
  payloadout += "}";
  payloadout += "}";
  
  char attributes[3000];
  payloadout.toCharArray(attributes, 3000);

  client.publish(pub_topic, attributes);


}
