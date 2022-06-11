#include <MQ135.h>
#include <WEMOS_SHT3X.h>
#include<string.h>

#define PIN_MQ135 A0
#define PM1PIN D6//DSM501A input D6 on ESP8266
#define PM25PIN D5


MQ135 mq135_sensor(PIN_MQ135);
SHT3X sht30(0x45);

float temperature = 21.0; // Assume current temperature. Recommended to measure with DHT22
float humidity = 25.0; // Assume current humidity. Recommended to measure with DHT22

int estado_co2 = 0;
int recebido_co2 = 0;
int ppm_co2 = -1;
int ppm_co2_tmp = 0;

byte buff[2];
unsigned long durationPM1;
unsigned long durationPM25;
unsigned long starttime;
unsigned long endtime;
unsigned long sampletime_ms = 30000;
unsigned long lowpulseoccupancyPM1 = 0;
unsigned long lowpulseoccupancyPM25 = 0;
int i = 0;

void setup() {
  Serial.begin(19200);
  pinMode(PM1PIN, INPUT);
  pinMode(PM25PIN, INPUT);
}
float calculateConcentration(long lowpulseInMicroSeconds, long durationinSeconds) {

  float ratio = (lowpulseInMicroSeconds / 1000000.0) / 30.0 * 100.0; //Calculate the ratio
  float concentration = 0.001915 * pow(ratio, 2) + 0.09522 * ratio - 0.04884; //Calculate the mg/m3
  Serial.print("lowpulseoccupancy:");
  Serial.print(lowpulseInMicroSeconds);
  Serial.print("    ratio:");
  Serial.print(ratio);
  Serial.print("    Concentration:");
  Serial.println(concentration);
  return concentration;
}
void loop() {
  //-- MQ-135
  float rzero = mq135_sensor.getRZero();
  float correctedRZero = mq135_sensor.getCorrectedRZero(temperature, humidity);
  float resistance = mq135_sensor.getResistance();
  float ppm = mq135_sensor.getPPM();
  float correctedPPM = mq135_sensor.getCorrectedPPM(temperature, humidity);

  durationPM1 = pulseIn(PM1PIN, LOW);
  durationPM25 = pulseIn(PM25PIN, LOW);

  lowpulseoccupancyPM1 += durationPM1;
  lowpulseoccupancyPM25 += durationPM25;

  float ratio1 = (lowpulseoccupancyPM1 / 1000000.0) / 30.0 * 100.0;
  float ratio2 = (lowpulseoccupancyPM25 / 1000000.0) / 30.0 * 100.0;

  float conPM1 = calculateConcentration(lowpulseoccupancyPM1, 30);
  float conPM25 = calculateConcentration(lowpulseoccupancyPM25, 30);
  float concentration2 = 1.1 * pow(ratio2, 3) - 3.8 * pow(ratio2, 2) + 520 * ratio2 + 0.62;
  float concentration1 = 1.1 * pow(ratio1, 3) - 3.8 * pow(ratio1, 2) + 520 * ratio1 + 0.62; // using spec sheet curve

  Serial.println("=-=-=-=-=-=-=-=-=-=-=-=-SHT30=-=-=-=-=-=-=-=-=-=-=-");
  if(sht30.get()==0){
    Serial.print("Temperature in Celsius : ");
    Serial.println(sht30.cTemp);
    Serial.print("Temperature in Fahrenheit : ");
    Serial.println(sht30.fTemp);
    Serial.print("Relative Humidity : ");
    Serial.println(sht30.humidity);
    Serial.println();
  }
  else
  {
    Serial.println("Error!");
  }
  Serial.println("=-=-=-=-=-=-=-=-=-=-=-=-MQ-135=-=-=-=-=-=-=-=-=-=-=-");
  Serial.print("MQ135 RZero: ");
  Serial.print(rzero);
  Serial.print("\n");
  Serial.print("Corrected RZero: ");
  Serial.print(correctedRZero);
  Serial.print("\n");
  Serial.print("Resistance: ");
  Serial.print(resistance);
  Serial.print("\n");
  Serial.print("PPM: ");
  Serial.print(ppm);
  Serial.print("\n");
  Serial.print("Corrected PPM: ");
  Serial.print(correctedPPM);
  Serial.println("ppm");
  Serial.println("=-=-=-=-=-=-=-=-=-=-=-=C02 T6615-=-=-=-=-=-=-=-=-=-=-=-=-");
  Serial.print("CO2: ");
  Serial.println(ppm_co2);
  leco2();
  Serial.println("=-=-=-=-=-=-=-=-=-=-=-=DSM501A-=-=-=-=-=-=-=-=-=-=-=-=-");
  Serial.print("PM1 ");
  Serial.println(conPM1);
  Serial.print("PM25 ");
  Serial.println(conPM25);

  Serial.print("concentration1 = ");
  Serial.print(concentration1);
  Serial.println(" pcs/0.01cf");

  Serial.print("concentration2 = ");
  Serial.print(concentration2);
  Serial.println(" pcs/0.01cf");

  if (concentration1 < 1000) {
    Serial.println("LIMPO");
  }
  if (concentration1 > 1000 && concentration1 < 10000) {
    Serial.println("BOM");
  }

  if (concentration1 > 10000 && concentration1 < 20000) {
    Serial.println("ACEITÁVEL");
  }
  if (concentration1 > 20000 && concentration1 < 50000) {
    Serial.println("PESADA");
  }

  if (concentration1 > 50000 ) {
    Serial.println("PERIGO");

  }
  lowpulseoccupancyPM1 = 0;
  lowpulseoccupancyPM25 = 0;

  delay(1000);
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
  while (Serial.available())
  {
    recebido_co2 = Serial.read();
    //Serial.println(recebido_co2);
    if (recebido_co2 == 255 && estado_co2 == 0)
    {
      estado_co2++;
    }
    else if (recebido_co2 == 250 && estado_co2 == 1)
    {
      estado_co2++;
    }
    else if (recebido_co2 == 2 && estado_co2 == 2)
    {
      estado_co2++;
    }
    else if (estado_co2 == 3)
    {
      ppm_co2_tmp = recebido_co2 * 255;
      estado_co2++;
    }
    else if (estado_co2 == 4)
    {
      ppm_co2_tmp += recebido_co2;
      estado_co2 = 0;
      ppm_co2 = ppm_co2_tmp;
    }
    else
    {
      estado_co2 = 0;
    }
  }
}
