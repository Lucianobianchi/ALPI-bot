import platform

import time
import datetime
from struct import *
import struct
import sys
import os
import select
import socket
import signal
import time
from gpiozero import Button

from connection import MCast
from connection import SerialConnection
from connection import Surrogator
from telemetry import TelemetryLoader
from motor import SerialMotor
from motor import SerialReel

# --- Disabling this for now, it was giving me some headaches
# First create a witness token to guarantee only one instance running
# if (os.access("running.wt", os.R_OK)):
#     print('Another instance is running. Cancelling.')
#     quit(1)
runningtoken = open('running.wt', 'w')

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

runningtoken.write(st)
runningtoken.close()

### Camera Streaming ###
system_platform = platform.system()
if system_platform == "Darwin":
  import FFMPegStreamer as pcs
else:
  import H264Streamer as pcs

dosomestreaming = False

vst = pcs.H264VideoStreamer()
if dosomestreaming:
  try:
    vst.startAndConnect()
  except Exception as e:
    print('Error starting H264 stream thread:'+e)


### Remote controller server for BotController.py ###
print('Starting up Controller Server on 0.0.0.0, port 30001')
server_address = ('0.0.0.0', 30001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind(server_address)
sur = Surrogator(sock)

### Motors and Reels connections ###
connection = SerialConnection()
motors = SerialMotor(connection=connection)
reels = SerialReel(connection=connection)

### Sensors - Telemetry ###
sensors = TelemetryLoader(connection)

### Stop all motors when process is killed ###
def terminate():
  print('Stopping ALPIBot')

  try:
    motors.stop()
    reels.stop()
  finally:
    os.remove('running.wt')

  print('ALPIBot has stopped.')
  exit(0)


signal.signal(signal.SIGINT, lambda signum, frame: terminate())
signal.signal(signal.SIGTERM, lambda signum, frame: terminate())

### Hardware buttons ###
RED_BUTTON = Button(2)
BLUE_BUTTON = Button(3)

RED_BUTTON.when_pressed = motors.stop
RED_BUTTON.when_released = reels.stop

BLUE_BUTTON.when_pressed = lambda: reels.both(200)
BLUE_BUTTON.when_released = reels.stop

### Control Loop ###
print('ALPIBot ready to follow!')
autonomous = False
# Live
while True:
  try:
    data = ''
    # TCP/IP server is configured as non-blocking
    sur.getmessage()

    cmd = sur.command
    cmd_data, address = sur.data, sur.address
    
    if cmd == 'A':
      if (len(sur.message) == 5):
        # Sending the message that was received.
        print(sur.message)
        connection.send(sur.message)
        sur.message = ''

    elif cmd == 'U':
      if cmd_data == 'M':
        autonomous = not autonomous
        if autonomous:
          print('Auto mode: ON')
        else:
          print('Auto mode: OFF')

      if autonomous:
        continue
      
      # Manual commands
      if cmd_data == 'k':
        reels.left(200)
      elif cmd_data == 'l':
        reels.right(200)
      elif cmd_data == 'r':
        reels.both(200)

      elif cmd_data == ' ':
        motors.stop()
        reels.stop()

      elif cmd_data == 'w':
        motors.both(100)
      elif cmd_data == 's':
        motors.both(-100)
      elif cmd_data == 'd':
        motors.left(100)
        motors.right(-100)
      elif cmd_data == 'a':
        motors.left(-100)
        motors.right(100)
      
      elif cmd_data == 'p':
        sdata = sensors.poll(frequency = 1, length = 1)
        print(sdata)
      elif cmd_data == 'X':
        break

  except Exception as err:
    print("Error:" + str(err))
    print("Waiting for serial connection to reestablish...")
    connection.reconnect()

  sys.stdout.flush()  # for service to print logs

vst.keeprunning = False
vst.interrupt()
sur.keeprunning = False

# When everything done, release the capture
sock.close()
terminate()
