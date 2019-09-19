#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("ALPI Bot motors, alive and well");
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
    case 116: // 't'
      // Telemetry data
      Serial.print("Telemetry!")
    default:
      Serial.println("Unsupported command: ");
      Serial.println(cmd);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read(); // read the incoming byte:
    Serial.print(" Received:"); Serial.println(incomingByte);
    processCommand(incomingByte);
  }
}