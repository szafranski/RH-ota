#include <Wire.h>

#define SLAVE_ADDRESS 0x0a
int number = 0;
int state = 0;

void setup() {
pinMode(12, OUTPUT);
pinMode(13, OUTPUT);
digitalWrite(12, HIGH); // set the LED on
digitalWrite(13, HIGH); // set the LED on
// initialize i2c as slave
Wire.begin(SLAVE_ADDRESS);
// define callbacks for i2c communication
Wire.onReceive(receiveData);
Wire.onRequest(sendData);

}

void loop() {
delay(10);
}

// callback for received data
void receiveData(int byteCount){

while(Wire.available()) {
number = Wire.read();

if (number == (79, 1))
{
digitalWrite(12, HIGH); 
digitalWrite(13, HIGH); 
}
if (number == (79, 0)){
digitalWrite(12, LOW); 
digitalWrite(13, LOW); 

}
}

}

// callback for sending data
void sendData(){
Wire.write(number);
}
