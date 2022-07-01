#include <SoftwareSerial.h>
#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
#define DEBUG true;

const int comeInSensor = A0; //analog pin 0
const int comeOutSensor = A1;

// vars
int sensorStateIn = 0;     // current state of the sensor
int sensorStateOut = 0;     // current state of the sensor
int distance = 312;
int margin_delay = 800;

int max_count = 100;
int min_count = 0;

void setup() {
  // initialize the sensor pin and input
  pinMode(comeInSensor, INPUT);
  pinMode(comeOutSensor, INPUT);

  // initialize serial communication
  Serial.begin(9600);
}

char state;

void loop() {
  // read the sensor input pin:
  sensorStateIn = analogRead(comeInSensor);
  sensorStateOut = analogRead(comeOutSensor);
  state = 'n';
  
  if ( sensorStateIn > distance ) {
    state = 'i';
    callback();
    delay(margin_delay);
  }

  if( sensorStateOut > distance ){
    state = 'o';
    callback();
    delay(margin_delay);
  }
}

void callback(){
  Serial.write(state);
}