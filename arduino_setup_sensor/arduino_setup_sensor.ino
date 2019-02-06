int moist_sensor_pin = A0;
int moist_output_value ;

void setup() {
  Serial.begin(9600);
  
  delay(2000);

}

void loop() {
   moist_output_value= analogRead(moist_sensor_pin);

   moist_output_value = map(moist_output_value,550,0,0,100) + 86;

   Serial.print(moist_output_value);

   Serial.println("");

   delay(1000);

}
