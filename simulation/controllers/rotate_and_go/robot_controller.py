from controller import Robot, GPS, Supervisor
import numpy as np
from scipy.spatial import distance
 
TIME_STEP = 64
robot = Supervisor()

MAX_WHEEL_SPEED = 9.5

wheels = []
wheelsNames = ['left wheel motor', 'right wheel motor']
 
gps_anchors = []
gps_anchors_names = ['left_gps_sensor', 'right_gps_sensor']
 
for i in range(2):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
 
for i in range(2):
    gps_anchors.append(robot.getGPS(gps_anchors_names[i]))
    gps_anchors[i].enable(1)    
 
subject = robot.getFromDef('FOLLOWING')
 
def set_subject_velocity(vel):
    subject.setVelocity(vel + [0, 0, 0])
 
AUTO_MOVE_SUBJECT = True
# Subject automoves in a sin wave. A and f are amplitude and frequency of that wave function.
A = 0.01
f = 0.03
Vz = 0.01 # Forward velocity of the subject.
def subject_velocity(time):
    sinv = A * 2 * np.pi * np.cos(2 * np.pi * f * (time/1000))
    return [sinv, 0, Vz]
 
def get_thread_lengths():
    tpos = np.array(subject.getPosition())
    lpos = np.array(gps_anchors[0].getValues())
    rpos = np.array(gps_anchors[1].getValues())
    llen = distance.euclidean([lpos[0], lpos[2]], [tpos[0], tpos[2]])
    rlen = distance.euclidean([rpos[0], rpos[2]], [tpos[0], tpos[2]])
    return (llen, rlen)

init_r = 0
init_l = 0
def start(control_strategy):
    def get_d(llen, rlen):
        return (llen + rlen) / 2

    time = 0
    while robot.step(TIME_STEP) != -1:
        if time == 0:
            init_l, init_r = get_thread_lengths()

        time += TIME_STEP
        if AUTO_MOVE_SUBJECT:
            sv = subject_velocity(time)
            set_subject_velocity(sv)
 
        print("GPS VALUES")
        print(gps_anchors[0].getValues())
        print(gps_anchors[1].getValues())
        
        llen, rlen = get_thread_lengths()
        d_l = llen - init_l
        d_r = rlen - init_r
        print("Ds")
        print(d_l, d_r)

        v_l, v_r = control_strategy(d_l, d_r)

        v_l, v_r = min(v_l, MAX_WHEEL_SPEED), min(v_r, MAX_WHEEL_SPEED)

        print("Vs")
        print(v_l, v_r)
        wheels[0].setVelocity(v_l)
        wheels[1].setVelocity(v_r)