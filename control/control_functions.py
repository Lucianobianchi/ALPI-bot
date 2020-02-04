import numpy as np

REEL_RADIUS = 12.2  # mm

def distances(sensor_data):
  lr_pulses = sensor_data['leftReelEncoder']
  rr_pulses = sensor_data['rightReelEncoder']

  l_distance = lr_pulses * (2 * np.pi * (REEL_RADIUS / 1000)) / 25.0
  r_distance = rr_pulses * (2 * np.pi * (REEL_RADIUS / 1000)) / 27.0
  return (l_distance, r_distance)

def dmean(d_l, d_r):
  return (d_l + d_r) / 2

MAX_SPEED = 10
MIN_MOTOR_V = 18
MAX_MOTOR_V = 255

def to_motor_power(vel):
  # vel = min(vel, MAX_SPEED)
  return round(vel * (MAX_MOTOR_V - MIN_MOTOR_V) / MAX_SPEED) + MIN_MOTOR_V

CV = 10
CR = 15
D_OFFSET = 0.0001

def follow_turn(sensor_data):
  sensor_data = sensor_data[0]
  d_l, d_r = distances(sensor_data)
  dm = dmean(d_l, d_r)
  if dm < D_OFFSET:
    return (0, 0)

  vtar = CV * (dm - D_OFFSET)
  v_l = vtar + CR * (d_l - d_r)
  v_r = vtar - CR * (d_l - d_r)
  return map(to_motor_power, [v_l, v_r])

CV = 35
CR = 10
BASE_VR = 0.3
DM_OFFSET = 0.0001
DT_OFFSET = 0.05

def rotate_go(sensor_data):
  sensor_data = sensor_data[0]
  d_l, d_r = distances(sensor_data)
  dt = d_l - d_r
  dm = dmean(d_l, d_r)
  if abs(dt) > DT_OFFSET:
    vr = BASE_VR + CR * (abs(dt) - DT_OFFSET)
    if d_l > d_r:  # Rotate clockwise
      return map(to_motor_power, (vr, -vr))
    else:  # Rotate counterclockwise
      return map(to_motor_power, (-vr, vr))
  elif dm > DM_OFFSET:  # Go forward
    vf = CV * (dm - DM_OFFSET)
    return map(to_motor_power, (vf, vf))
  else:  # Stop
    return (0, 0)
