from controller import Robot, GPS, Supervisor
import numpy as np
from scipy.spatial import distance
import csv
import leader_path

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

# Get velocity, get orientation, in case I can use this data
# bot_node = robot.getFromDef('ALPIBOT')
# print(bot_node.getOrientation())
# print(bot_node.getVelocity())

def set_subject_velocity(vel):
    subject.setVelocity(vel + [0, 0, 0])

def set_subject_position(pos):
    subject_t_field.setSFVec3f(pos)
 
DEBUG = False

RECORD = False
record_filename = 'sample.csv' 
if RECORD:
    record_file = open(record_filename, 'x', newline='\n')
    record_writer = csv.writer(record_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    record_writer.writerow(['time', 'd_l', 'd_r', 'llen', 'rlen', 'left_gps_x', 'left_gps_y', 'left_gps_z', \
    'right_gps_x', 'right_gps_y', 'right_gps_z', 'subject_x', 'subject_y', 'subject_z', 'v_r', 'v_l'])

AUTO_MOVE_SUBJECT = True
x0 = 0
y0 = 0.06
z0 = 0.5
GERONO_A = 2
GERONO_N = 4000
GERONO_TS = leader_path.generate_gerono_lemniscate_t(GERONO_N)

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
            t = GERONO_TS[time // TIME_STEP]
            z, x = leader_path.gerono_lemniscate_xy(t, GERONO_A)
            x = x + x0
            y = y0
            z = z + z0
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

        if RECORD:
            left_gps = gps_anchors[0].getValues()
            right_gps = gps_anchors[1].getValues()
            s_pos = subject.getPosition() 
            record_writer.writerow([time, d_l, d_r, llen, rlen, left_gps[0], left_gps[1], left_gps[2], \
            right_gps[0], right_gps[1], right_gps[2], s_pos[0], s_pos[1], s_pos[2], v_l, v_r])

        wheels[0].setVelocity(v_l)
        wheels[1].setVelocity(v_r)

    record.close()

def get_thread_lengths():
    tpos = np.array(subject.getPosition())
    lpos = np.array(gps_anchors[0].getValues())
    rpos = np.array(gps_anchors[1].getValues())
    llen = distance.euclidean([lpos[0], lpos[2]], [tpos[0], tpos[2]])
    rlen = distance.euclidean([rpos[0], rpos[2]], [tpos[0], tpos[2]])
    return (llen, rlen)
