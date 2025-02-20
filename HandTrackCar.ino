#include <SoftwareSerial.h>
SoftwareSerial bluetooth(3, 4); // (RX, TX) (pin Rx BT, pin Tx BT)

const int motor1EnablePin = 9;  // Enable pin for Motor 1
const int motor1Input1 = 8;     // Input 1 for Motor 1
const int motor1Input2 = 7;     // Input 2 for Motor 1

const int motor2EnablePin = 10; // Enable pin for Motor 2
const int motor2Input1 = 11;    // Input 1 for Motor 2
const int motor2Input2 = 12;    // Input 2 for Motor 2
const int speed =90;
char command; //Int to store app command state.

// Function to run both motors forward
void Forward() {
  digitalWrite(motor1Input1, HIGH);
  digitalWrite(motor1Input2, LOW);
  analogWrite(motor1EnablePin,speed);
   
  digitalWrite(motor2Input1, HIGH);
  digitalWrite(motor2Input2, LOW);
  analogWrite(motor2EnablePin,speed);
  }
  void back() {

  digitalWrite(motor1Input1, LOW);
  digitalWrite(motor1Input2, HIGH);
  analogWrite(motor1EnablePin,speed);
   
  digitalWrite(motor2Input1, LOW);
  digitalWrite(motor2Input2, HIGH);
  analogWrite(motor2EnablePin,speed);
  }



void left() {
digitalWrite(motor1Input1, HIGH);
digitalWrite( motor1Input2, LOW);
analogWrite(motor1EnablePin,90);
digitalWrite(motor2Input1, LOW);
 digitalWrite(motor2Input2, HIGH);
 analogWrite(motor2EnablePin,90);
}

void right() {
digitalWrite( motor2Input1, HIGH);
digitalWrite( motor2Input2, LOW);
analogWrite(motor2EnablePin,90);
digitalWrite(motor1Input1, LOW);
digitalWrite( motor1Input2, HIGH);
analogWrite(motor1EnablePin,90);
}

void Stop() {
  digitalWrite(motor1Input1, LOW);
  digitalWrite(motor1Input2, LOW);
  digitalWrite(motor2Input1, LOW);
  digitalWrite(motor2Input2, LOW);
}
void setup() {

pinMode(motor2EnablePin, OUTPUT);
pinMode(motor2Input1, OUTPUT);
pinMode(motor2Input2, OUTPUT);
pinMode(motor1EnablePin, OUTPUT);
pinMode(motor1Input1, OUTPUT);
pinMode(motor1Input2, OUTPUT);
  
  bluetooth.begin(9600);  //Set the baud rate to your Bluetooth module.
  Serial.begin(9600);
}

void loop() {
 
  if (bluetooth.available()>0) {
    command = bluetooth.read();
  
    
    switch (command) {
      case 'F':
        Forward();
        Serial.println(command);
        break;
      case 'B':
        back();
        Serial.println(command);
        break;
      case 'L':
        left();
        Serial.println(command);
        break;
      case 'R':
        right();
        Serial.println(command);
        break;
      case 'S':
        Stop();
        Serial.println(command);
        break;
    }
}
}
