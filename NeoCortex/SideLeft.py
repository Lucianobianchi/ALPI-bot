import MotorBridge
import time

motor = MotorBridge.MotorBridgeCape()
motor.DCMotorInit(1,1000)
motor.DCMotorInit(2,1000)
motor.DCMotorInit(3,1000)
motor.DCMotorInit(4,1000)

motor.DCMotorMove(1,2,190)
motor.DCMotorMove(2,1,190)
motor.DCMotorMove(3,2,190)
motor.DCMotorMove(4,1,190)
time.sleep(2)

motor.DCMotorStop(1)
motor.DCMotorStop(2)
motor.DCMotorStop(3)
motor.DCMotorStop(4)

