const int nbrSwitches                  = 2;
const int bumpSwitchPins[nbrSwitches]  = {24,33};
const int switchPin                    = 5; 
const int ledPin                       = 13;
const int leftMotorPins[]              = {27,30,32}; // marked wheel 1 on board
const int rightMotorPins[]             = {20,6,25};  // marked wheel 2 on board  (6 & 20 swapped in final brd)

#include "HUBeeBMDWheel.h"

HUBeeBMDWheel motor1Wheel;
HUBeeBMDWheel motor2Wheel;

void setup() {                
  motor1Wheel.setupPins(leftMotorPins[0],leftMotorPins[1],leftMotorPins[2]); 
  motor2Wheel.setupPins(rightMotorPins[0],rightMotorPins[1],rightMotorPins[2]);
}

// the loop routine runs over and over again forever:
void loop() {

  drive(0, 100);
//  delay(3000);
//  drive(1, 255);
//  delay(3000);
//  
//  stopRobot(); 
  delay(3000);

}

void drive(int robotDirection, int robotSpeed){
  
  motor1Wheel.setDirectionMode(robotDirection);
  motor2Wheel.setDirectionMode(not(robotDirection));

  motor1Wheel.setMotorPower(robotSpeed);
  motor2Wheel.setMotorPower(robotSpeed);

}

void turnLeft(){
  motor1Wheel.setDirectionMode(1);
  motor2Wheel.setDirectionMode(1);
  motor1Wheel.setMotorPower(100);
  motor2Wheel.setMotorPower(100);
}

void turnRight(){
  motor1Wheel.setDirectionMode(0);
  motor2Wheel.setDirectionMode(0);
  motor1Wheel.setMotorPower(100);
  motor2Wheel.setMotorPower(100);
}

void stopRobot(){
  motor2Wheel.stopMotor();
  motor1Wheel.stopMotor();
}

