/**
 *
 */

// Pins for the optical encoder inputs.
// The pin 2 and 3 are the interrupt pins 0 and 1 for Arduino UNO
#define LH_RENCODER_A 18
#define LH_RENCODER_B 30
#define RH_RENCODER_A 19
#define RH_RENCODER_B 31

// variables to store the number of encoder pulses
// for each motor
// volatile is used to indicate not to use cpu register and instead, use memory locations.
volatile  long leftReelCount = 0;
volatile  long rightReelCount = 0;

volatile int aRightVal;
volatile int aLeftVal;

volatile int pinARightLast;
volatile int pinALeftLast;


void leftReelEncoderEvent() {
  aLeftVal = digitalRead(LH_RENCODER_A);
  if (aLeftVal != pinALeftLast) { // Means the knob is rotating
    // if the knob is rotating, we need to determine direction
    // We do that by reading pin B.
    if (digitalRead(LH_RENCODER_B) != aLeftVal) {  // Means pin A Changed first - We're Rotating Clockwise
      leftReelCount ++;
    } else {// Otherwise B changed first and we're moving CCW
      leftReelCount--;
    }
  }
  pinALeftLast = aLeftVal; 
}

// In order to have positive values for both encoders, I need to CHANGE how the counter is increased because 
// one encoder is moving forward while the other is moving backwards (they are inverted in the robot).
void rightReelEncoderEvent() {
  aRightVal = digitalRead(RH_RENCODER_A);
  if (aRightVal != pinARightLast) { // Means the knob is rotating
    // if the knob is rotating, we need to determine direction
    // We do that by reading pin B.
    if (digitalRead(RH_RENCODER_B) != aRightVal) {  // Means pin A Changed first - We're Rotating Clockwise
      rightReelCount--;
    } else {// Otherwise B changed first and we're moving CCW
      rightReelCount++;
    }
  }
  pinARightLast = aRightVal; 
}

void setupReelEncoders()
{
  pinMode(LH_RENCODER_A, INPUT);
  pinMode(LH_RENCODER_B, INPUT);
  pinMode(RH_RENCODER_A, INPUT);
  pinMode(RH_RENCODER_B, INPUT);
  
  // initialize hardware interrupts
  attachInterrupt(digitalPinToInterrupt(LH_RENCODER_A), leftReelEncoderEvent, CHANGE);
  attachInterrupt(digitalPinToInterrupt(RH_RENCODER_A), rightReelEncoderEvent, CHANGE);  
}

void loopReelEncoders()
{
  sensor.righReelEncoder = rightReelCount;
  sensor.leftReelEncoder = leftReelCount;  

  if (debug)
  {
    Serial.print("L:");Serial.print(leftReelCount);Serial.print("-R:");Serial.println(rightReelCount);
  }
}

void resetReelEncoders()
{
  leftReelCount = 0; 
  rightReelCount = 0;
  
}

