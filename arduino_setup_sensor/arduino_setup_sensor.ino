#include <Wire.h>

int moist_sensor_pin = A0;
int ph_fertility_pin = A1;
int moist_output_value ;
float ph;
int  fertility;

void setup() {
  Serial.begin(9600);
  
  delay(2000);

}

void loop() {
  
   moist_output_value= analogRead(moist_sensor_pin);

   moist_output_value = map(moist_output_value,550 ,0,0,100) + 84;

   fertility = (-readFertility() +123)*2;
   ph = readPH() + 7;

   Serial.print(moist_output_value);

   Serial.print(" ");

   Serial.print(ph);

   Serial.print(" ");

   Serial.print(fertility);

   Serial.println("");

   delay(1000);

}

int readFertility()
{int i,Fertility;
   Fertility = 0; 
   for(i=0;i<10;i++){Fertility = Fertility + analogRead(ph_fertility_pin);delay(1);}
   Fertility = Fertility/10;
   if(Fertility >= 480){Fertility = ((Fertility - 480)/10) + 93;}else
   if(Fertility >= 360){Fertility = ((Fertility - 360)/7.5) + 77;}else
   if(Fertility >= 275){Fertility = ((Fertility - 275)/5) + 59;}else
   if(Fertility >= 200){Fertility = ((Fertility - 200)/6.25) + 47;}else
   if(Fertility >= 125){Fertility = ((Fertility - 125)/5.3) + 31;}else
   if(Fertility >= 65){Fertility = ((Fertility - 65)/4) + 16;}else
   if(Fertility >=  0){Fertility = ((Fertility - 0)/3.75) + 0;}
   return(Fertility);
}
//----------------------------------------------------------------------------
float readPH()
{int i;
 float PH;
   PH = 0;
   for(i=0;i<10;i++){PH  = PH + analogRead(ph_fertility_pin);delay(10); } 
   PH       = PH/10;
   if(PH >= 480){PH = (10-(PH - 480)/14);}else
   if(PH >= 360){PH = (20-(PH - 360)/12);}else
   if(PH >= 275){PH = (30-(PH - 275)/8.5);}else
   if(PH >= 200){PH = (40-(PH - 200)/7.5);}else
   if(PH >= 125){PH = (50-(PH - 125)/8.5);}else
   if(PH >= 65 ){PH = (60-(PH - 60)/6.5);}else
   if(PH >=  0 ){PH = (70-(PH - 0)/6.0);}
   return(PH/10);
}
