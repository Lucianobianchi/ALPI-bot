import numpy as np

REEL_RADIUS = 12.2 #mm

def _distance(pulses):
  return pulses * (2 * np.pi * REEL_RADIUS) / 36.0

def distances(sensor_data):
  lr_pulses = sensor_data['leftReelEncoder']
  rr_pulses = sensor_data['rightReelEncoder']
  return (_distance(lr_pulses), _distance(rr_pulses))

def follow_turn(sensor_data):
  sensor_data = sensor_data[0]
  d_l, d_r = distances(sensor_data)
  print('Follow Turn!')
  print('D left:', d_l, 'mm')
  print('D right:', d_r, 'mm')
  return [d_l, d_r]

def rotate_go(sensor_data):
  sensor_data = sensor_data[0]
  d_l, d_r = distances(sensor_data)
  print('Rotate GO!')
  print('D left:', d_l, 'mm')
  print('D right:', d_r, 'mm')
  return [d_l, d_r]