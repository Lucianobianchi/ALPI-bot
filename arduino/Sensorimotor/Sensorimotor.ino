/**
 * ALPIBot
 */

#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *rightMotor = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(2);
Adafruit_DCMotor *rightReel = AFMS.getMotor(4);
Adafruit_DCMotor *leftReel = AFMS.getMotor(3);

bool debug = false;
bool debugSensor = false;
String codeversion="1.0";

struct sensortype
{
  long code;
  long rightEncoder;
  long leftEncoder;
  long rightReelEncoder;
  long leftReelEncoder;
  float voltage;
  float current;
  long freq;
  long counter;
} sensor;

struct botStateType {
  long leftSpeed;
  long rightSpeed;
  long reelSpeed;
  long lastReelTime;
} botState;

int StateMachine(int state, int controlvalue)
{
  static int previousState = 0;
  switch (state)
  {
    case 0x01: // left motor forward
      moveLeft(controlvalue);
      break;
    case 0x02: // right motor forward
      moveRight(controlvalue);
      break;
    case 0x03: // left motor backwards
      moveLeft(-controlvalue);
      break; 
    case 0x04: // right motor backwards
      moveRight(-controlvalue);
      break;   
    case 0x05: // both motors forward
      moveRight(controlvalue);
      moveLeft(controlvalue);
      break;  
    case 0x06: // both motors backwards
      moveRight(-controlvalue);
      moveLeft(-controlvalue);
      break;  
    case 0x07: // stop both motors
      stopLeft();
      stopRight();
      break;
    case 0x0A: // left reel
      leftReel->setSpeed(controlvalue);
      leftReel->run(FORWARD);
      break;   
    case 0x0B: // right reel
      rightReel->setSpeed(controlvalue);
      rightReel->run(FORWARD);
      break;
    case 0x0C: // both reels
      leftReel->setSpeed(controlvalue);
      rightReel->setSpeed(controlvalue);
      rightReel->run(FORWARD);
      leftReel->run(FORWARD);
      botState.reelSpeed = controlvalue;
      break;
    case 0x0D: // stop reels
      leftReel->run(RELEASE);
      rightReel->run(RELEASE);
      botState.reelSpeed = 0;
      break;
    case 0x0F: // stop all motors and reels
      leftMotor->run(RELEASE);
      rightMotor->run(RELEASE);
      leftReel->run(RELEASE);
      rightReel->run(RELEASE);
      botState.leftSpeed = 0;
      botState.rightSpeed = 0;
      botState.reelSpeed = 0;
    default:
      // Do Nothing
      state = 0;
      break;
  }  
  
  previousState = state;
  return state;
}

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.print("AlpiBot v");Serial.println(codeversion);
  stopBurst();
    
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  // Set the speed to start, from 0 (off) to 255 (max speed)
  rightMotor->setSpeed(1);
  rightMotor->run(FORWARD);
  // turn on motor
  rightMotor->run(RELEASE);

  leftMotor->setSpeed(1);
  leftMotor->run(FORWARD);
  // turn on motor
  leftMotor->run(RELEASE);

  leftReel->setSpeed(1);
  leftReel->run(FORWARD);
  // turn on motor
  leftReel->run(RELEASE);

  rightReel->setSpeed(1);
  rightReel->run(FORWARD);
  // turn on motor
  rightReel->run(RELEASE);

  memset(&sensor, 0, sizeof(sensor));
  memset(&botState, 0, sizeof(botState));
  
  setupMotorEncoders();
  setupReelEncoders();
}


int incomingByte = 0;

char buffer[6];
char actionBuf[3];

void readcommand(int &action, int &controlvalue)
{
  // Format ACCNNN, 'A', CC is command, NNN is the controlvalue.
  memset(buffer, 0, 6);
  memset(actionBuf, 0, 3);
  int readbytes = Serial.readBytes(buffer, 5);

  if (readbytes == 5) {
    actionBuf[0] = buffer[0];
    actionBuf[1] = buffer[1];
    
    action = strtol(actionBuf, NULL, 16);
    controlvalue = atoi(buffer + 2);
    
    if (debug) {
      Serial.print("Action:"); Serial.print(action); Serial.print("|"); Serial.println(controlvalue);
    }
  }
}

// the loop routine runs over and over again forever:
void loop() {
  unsigned long currentMillis = millis();
  int incomingByte;
  int action, state, controlvalue;
  
  sensor.freq = frequency();
  burstSensors();

  bool doaction = false;
  
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    doaction = true;
  }

  if (doaction) 
  {
    switch (incomingByte) {
      case 'D':
        debug = (!debug);
        break;
      case 'C': 
        debugSensor = (!debugSensor);
        break;
      case 'A': // motor controls
        readcommand(action, controlvalue);
        state = action; // let StateMachine process the action
        break;
      case 'S': // sensor controls
        readcommand(action, controlvalue);
        state = 0;
        switch (action) {
          case 0x01:
            startBurst(controlvalue);
            break;
          case 0x02:
            stopBurst();
            break;
          case 0x1A:
            // Determines the amount of frames to send in a burst.
            setBurstSize(controlvalue);
            break;
          case 0x1B:
            // Determines the updating frequency in relation to current arduino frequency (which is variable)
            // For instance, 1 means the same frequency, 2 means half the frequency: 1/freq
            setUpdateFreq(controlvalue);
            break;
          case 0x1C:
            setCode(controlvalue);
            break;
          case 0x21:
            sendPayloadSize();
            break;
          case 0x22:
            transmitSensors();
            break;
        }
    }
  }

  loopEncoders();
  loopReelEncoders();

  StateMachine(state, controlvalue);

  reelsMotors();

  if (debug) {
      Serial.print("RW:"); Serial.println(sensor.rightEncoder);
      Serial.print("LW:"); Serial.println(sensor.leftEncoder);
      Serial.print("RR:"); Serial.println(sensor.rightReelEncoder);
      Serial.print("LR:"); Serial.println(sensor.leftReelEncoder);
  }
}
