/**
    ALPIBot
    
    Basic Program to read commands from Serial and move the 4 motors accordingly.

    TODO [easy]: debug mode, get telemetry
    TODO [hard]: research the best way to move motors (indefinitely vs fixed time per command)
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

bool debug = false;

int MIN_SPEED = 0;
int INITIAL_SPEED = 30;
int MAX_SPEED = 160;
// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor* motors[] = {AFMS.getMotor(1), AFMS.getMotor(2), AFMS.getMotor(3), AFMS.getMotor(4)};

void moveAllInDirection(int direction) {
  for (int i = 0; i < 4; i++) {
    motors[i]->run(direction);
  }
}

void rotateRight() {
   motors[0]->run(FORWARD);
   motors[2]->run(FORWARD);
   motors[1]->run(BACKWARD);
   motors[3]->run(BACKWARD);
}

void rotateLeft() {
   motors[0]->run(BACKWARD);
   motors[2]->run(BACKWARD);
   motors[1]->run(FORWARD);
   motors[3]->run(FORWARD);
}

void processCommand(int cmd) {
  switch(cmd) {
    case 119: // 'w'
      Serial.println("Moving forward");
      moveAllInDirection(FORWARD);
      break;
    case 115: // 's'
      Serial.println("Moving backwards");
      moveAllInDirection(BACKWARD);
      break;
    case 107: // 'k'
      Serial.println("Rotating left");
      rotateLeft();
      break;
    case 108: // 'l'
      Serial.println("Rotating right");
      rotateRight();
      break;
    case 120: // 'x'
      Serial.println("Stopping all motors");
      moveAllInDirection(RELEASE);
      break;
    default:
      Serial.println("Unsupported command: ");
      Serial.println(cmd);
  }
}

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("ALPI Bot motors, alive and well");

  AFMS.begin();  // create with the default frequency 1.6KHz

  for (int i = 0; i < 4; i++) {
    motors[i]->setSpeed(INITIAL_SPEED);
    motors[i]->run(RELEASE);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read(); // read the incoming byte:
    Serial.print(" Received:"); Serial.println(incomingByte);
    processCommand(incomingByte);
  }
}
