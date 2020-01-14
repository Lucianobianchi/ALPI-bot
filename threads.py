from connection import SerialConnection
from telemetry import TelemetryLoader
from motor import SerialReel
import matplotlib.pyplot as plt
import sched
from control import distances

serial = SerialConnection()
reels = SerialReel(connection = serial)
loader = TelemetryLoader(serial)

REEL_POW = 200
MOVE_REELS = False
UPDATE_SPEED = 0.05 # s
PLOT = False

reels.stop()
if MOVE_REELS:
  reels.both(200)

threads = ['Left', 'Right']
lengths = [0, 0]

if PLOT:
  fig, ax = plt.subplots()
  bars = ax.bar(threads, lengths)
  ax.set_xlabel('Threads')
  ax.set_ylabel('Length [mm]')
  ax.set_title('Reel threads lengths')

  plt.ylim([-50, 100])
  left_bar = bars[0]
  right_bar = bars[1]
  fig.canvas.draw()

s = sched.scheduler(time.time, time.sleep)
def update(sc): 
  sensor_data = loader.poll(frequency = 1, length = 1)
  # print(sensor_data)
  ld, rd = distances(sensor_data[0])

  if PLOT: 
    left_bar.set_height(ld)
    right_bar.set_height(rd)
    plt.draw()
    plt.pause(0.001)

  print(f"Left: {ld} mm")
  print(f"Right: {rd} mm")

  s.enter(UPDATE_SPEED, 1, update, (sc,))

s.enter(0, 1, update, (s,))
s.run()