import time

import os
import sys
# sys.path.append(os.path.abspath('./motor'))

class MotorController:
    def __init__(self, *, pwmduty = 190, mock = False):
        if mock:
            import motor.MockMotorBridge as MockMotorBridge
            self.motor = MockMotorBridge.MotorBridgeCape()
        else:
            import MotorBridge
            self.motor = MotorBridge.MotorBridgeCape()

        self.pwmduty = pwmduty
        self.motor.DCMotorInit(1,1000)
        self.motor.DCMotorInit(2,1000)
        self.motor.DCMotorInit(3,1000)
        self.motor.DCMotorInit(4,1000)

    def stop(self):
        for i in range(1, 5):
            self.motor.DCMotorStop(i)

    def move_forward(self):
        for i in range(1, 5):
            self.motor.DCMotorMove(i, 1, self.pwmduty)

    def move_backwards(self):
        for i in range(1, 5):
            self.motor.DCMotorMove(i, 2, self.pwmduty)
    
    def move_left(self):
        self.motor.DCMotorMove(1, 2, self.pwmduty)
        self.motor.DCMotorMove(2, 1, self.pwmduty)
        self.motor.DCMotorMove(3, 2, self.pwmduty)
        self.motor.DCMotorMove(4, 1, self.pwmduty)

    def move_right(self):
        self.motor.DCMotorMove(1, 1, self.pwmduty)
        self.motor.DCMotorMove(2, 2, self.pwmduty)
        self.motor.DCMotorMove(3, 1, self.pwmduty)
        self.motor.DCMotorMove(4, 2, self.pwmduty)

    def rotate_left(self):
        self.motor.DCMotorMove(1, 2, self.pwmduty)
        self.motor.DCMotorMove(2, 1, self.pwmduty)
        self.motor.DCMotorMove(3, 1, self.pwmduty)
        self.motor.DCMotorMove(4, 2, self.pwmduty)

    def rotate_right(self):
        self.motor.DCMotorMove(1, 1, self.pwmduty)
        self.motor.DCMotorMove(2, 2, self.pwmduty)
        self.motor.DCMotorMove(3, 2, self.pwmduty)
        self.motor.DCMotorMove(4, 1, self.pwmduty)

    def increase_duty(self):
        self.pwmduty = self.pwmduty + 10
    
    def decrease_duty(self):
        self.pwmduty = self.pwmduty - 10