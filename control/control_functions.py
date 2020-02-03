import numpy as np

REEL_RADIUS = 12.2 #mm

def _distance(pulses): # distance in meters
  return pulses * (2 * np.pi * (REEL_RADIUS/1000)) / 36.0

def distances(sensor_data):
  lr_pulses = sensor_data['leftReelEncoder']
  rr_pulses = sensor_data['rightReelEncoder']
  return (_distance(lr_pulses), _distance(rr_pulses))

def dmean(d_l, d_r):
    return (d_l + d_r) / 2

MAX_SPEED = 10
MAX_MOTOR_V = 255
def to_motor_power(vel):
  vel = min(vel, MAX_SPEED)
  if vel < 0:
    return 0
  return round((vel / MAX_SPEED) * MAX_MOTOR_V)

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
  print('Follow Turn!')
  print('D left:', d_l, 'mm')
  print('D right:', d_r, 'mm')
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
      if d_l > d_r: # Rotate clockwise
          return map(to_motor_power, (vr, -vr))
      else: # Rotate counterclockwise
          return map(to_motor_power, (-vr, vr))
  elif dm > DM_OFFSET: # Go forward
      vf = CV * (dm - DM_OFFSET)
      return map(to_motor_power, (vf, vf))
  else: # Stop
      return (0, 0)