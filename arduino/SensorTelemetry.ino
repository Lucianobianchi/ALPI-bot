#define MAX_SIZE_SENSOR_BURST 100

/* Returns the amount of loops the arduino made in the last second */
long frequency() {
  static unsigned long lastFreqValue = 0;
  static unsigned long freqCounter = 0;
  static unsigned long prevMillis = millis();

  unsigned long currMillis = millis();

  if (currMillis - prevMillis > 1000) {
    prevMillis = currMillis;
    lastFreqValue = freqCounter;
    freqCounter = 0;
  } else {
    freqCounter++;
  }
  
  return lastFreqValue;
}

bool sensorburst = false;
unsigned long transmittedCounter = 0;
int burstsize = MAX_SIZE_SENSOR_BURST;

int updateFreq = 1;

void setBurstSize(int val) {
  burstsize = min(MAX_SIZE_SENSOR_BURST, val);
  if (debugSensor) {
    Serial.print("Burst size set to: "); Serial.println(burstsize);
  }
}

void setUpdateFreq(int val) {
  updateFreq = val;
  if (debugSensor) {
    Serial.print("Update frequency set to: "); Serial.println(val);
  }
}

void setCode(int val) {
  sensor.code = val;
  if (debugSensor) {
    Serial.print("Code set to: "); Serial.println(val);
  }
}

void burstSensors() {
  if (!sensorburst)
    return;

  sensor.counter++;
  transmittedCounter++;
  
  if (transmittedCounter % updateFreq == 0) {
    transmitSensors();
  }
  if (transmittedCounter >= burstsize) {
    stopBurst();
  }
}

void startBurst(int val) {
  if (val != 0)
    setBurstSize(val);
    
  sensorburst = true;
  
  // Reset counter to avoid loosing data.
  transmittedCounter = 0;
  sensor.counter = 0;
}

void stopBurst() {
  sensorburst = false;
  transmittedCounter = 0;
  sensor.counter = 0;
}

void sendPayloadSize() {
  int len = sizeof(sensor);
  Serial.write(len);
}

/* Sends all the sensor data as a payload via Serial */
void transmitSensors() {
  int len = sizeof(sensor);
  char aux[len];
  memcpy(&aux, &sensor, len);

  if (debugSensor) {
    Serial.print("Len:"); Serial.println(len);
    Serial.print("Counter:"); Serial.println(sensor.counter);
    Serial.print("Freq:"); Serial.println(sensor.freq);
    Serial.print("RW:"); Serial.println(sensor.rightEncoder);
    Serial.print("LW:"); Serial.println(sensor.leftEncoder);
    Serial.print("RR:"); Serial.println(sensor.rightReelEncoder);
    Serial.print("LR:"); Serial.println(sensor.leftReelEncoder);
  }
  
  Serial.write('{');
  Serial.write((uint8_t *) &aux, len);
  Serial.write('}');
}
