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
subject_t_field = subject.getField('translation')

def set_subject_velocity(vel):
    subject.setVelocity(vel + [0, 0, 0])

def set_subject_position(pos):
    subject_t_field.setSFVec3f(pos)
 
DEBUG = False
AUTO_MOVE_SUBJECT = True
# Subject automoves in a sin wave. A and f are amplitude and frequency of that wave function.
A = 1.5
T = 2
Vz = 1E-5 # Forward velocity of the subject.
x0 = 0
y0 = 0.06
z0 = 0.5
 
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
            z = z0 + Vz * time
            x = x0 + A * np.sin(2 * np.pi * (Vz * time) / T)
            set_subject_position([x, y0, z])
 
        if DEBUG:
            print("GPS VALUES")
            print(gps_anchors[0].getValues())
            print(gps_anchors[1].getValues())
        
        llen, rlen = get_thread_lengths()
        d_l = llen - init_l
        d_r = rlen - init_r

        if DEBUG:
            print("Ds")
            print(d_l, d_r)

        v_l, v_r = control_strategy(d_l, d_r)

        v_l, v_r = min(v_l, MAX_WHEEL_SPEED), min(v_r, MAX_WHEEL_SPEED)

        if DEBUG:
            print("Vs")
            print(v_l, v_r)

        wheels[0].setVelocity(v_l)
        wheels[1].setVelocity(v_r)