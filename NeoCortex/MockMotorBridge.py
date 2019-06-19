import time 

def WriteByte(Reg,Value):
    pass

def WriteHalfWord(Reg,Value):
    pass
    
def WriteOneWord(Reg,Value):
    pass

def SetDefault():
    pass

class MotorBridgeCape:
    def __init__(self):
        pass
        
    # init stepper motor A
    def StepperMotorAInit(self):
        pass
        
    # MoveSteps > 0 CW 
    # MoveSteps < 0 CCW
    # StepDelayTime : delay time for every step. uint us
    def StepperMotorAMove(self,MoveSteps,StepDelayTime):   
        pass
        
        
    # init stepper motor B
    def StepperMotorBInit(self):
        pass
        
    # MoveSteps > 0 CW 
    # MoveSteps < 0 CCW
    # StepDelayTime : delay time for every step. uint us
    def StepperMotorBMove(self,MoveSteps,StepDelayTime):
        pass
        
    # Init DC Motor
    def DCMotorInit(self,MotorName,Frequency):
        pass

    def DCMotorMove(self, MotorName,Direction,PWMDuty):
        pass
            
    # Stop the DC motor
    def DCMotorStop(self, MotorName):
        pass
    
    # init the Servo 
    def ServoInit(self,ServoName,Frequency):
        pass
              
    def ServoMoveAngle(self,ServoName,Angle):
        pass
            
def myloop():
    print 'Hello From MotorBridge'
    time.sleep(1)
    motor.StepperMotorBMove(-1000,1000) # 20 steppers  1000us every step
    time.sleep(1)
    motor.StepperMotorBMove(1000,1000)  # 20 steppers  1000us every step
    myloop()

if __name__=="__main__":
    motor = MotorBridgeCape()
    motor.StepperMotorBInit()
    motor.StepperMotorBMove(1000,1000) # 20 steppers  1000us every step
    myloop()
