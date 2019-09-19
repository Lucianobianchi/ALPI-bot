/**
    Handling of DC motors connected to the MotorShield
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

void initMotors() {
  AFMS.begin();  // create with the default frequency 1.6KHz

  for (int i = 0; i < 4; i++) {
    motors[i]->setSpeed(INITIAL_SPEED);
    motors[i]->run(RELEASE);
  }
}

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