int estado_co2=0;
int recebido_co2=0;
int ppm_co2=-1;
int ppm_co2_tmp=0;

void setup() {
  Serial.begin(19200);
}


void loop() {
    leco2();
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