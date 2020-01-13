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
from connection.SerialConnection import SerialConnection
from connection.Surrogator import Surrogator
from motor.SerialMotor import SerialMotor
from motor.SerialReel import SerialReel
from sensors.SensorimotorCortex import SensorimotorCortex

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
if (dosomestreaming):
  try:
    vst.startAndConnect()
    pass
  except Exception as e:
    print('Error starting H264 stream thread:'+e)


### Remote controller server for BotController.py ###
print('Starting up Controller Server on 0.0.0.0, port 30001')
server_address = ('0.0.0.0', 30001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
sur = Surrogator(sock)

### Motors and Reels connections ###
connection = SerialConnection()
motors = SerialMotor(connection=connection)
reels = SerialReel(connection=connection)

### Sensors - Telemetry ###
# Enables the sensor telemetry.
# Arduinos will send telemetry data that will be sent to listening servers.
sensesensor = False
# Connect remotely to any client that is waiting for sensor loggers.
sensorimotor = SensorimotorCortex(connection, 'sensorimotor', 24)
sensorimotor.init()
sensorimotor.start()
sensorimotor.sensorlocalburst = 1000
sensorimotor.sensorburst = 100
sensorimotor.updatefreq = 10
sensorimotor.cleanbuffer()

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

RED_BUTTON.when_pressed = lambda: motors.stop()
RED_BUTTON.when_released = lambda: reels.stop()

BLUE_BUTTON.when_pressed = lambda: reels.both(200)
BLUE_BUTTON.when_released = lambda: reels.stop()

### Control Loop ###
print('ALPIBot ready to follow!')
# Live
while(True):
  try:
    data = ''
    # TCP/IP server is configured as non-blocking
    sur.getmessage()

    cmd = sur.command
    cmd_data, address = sur.data, sur.address

    # If someone asked for it, send sensor information.
    if (sensesensor):
      sens = sensorimotor.picksensorsample()

      if (sens != None):
        # Check where to put the value
        sensorimotor.repack([0], [fps.fps])
        sensorimotor.send(sensorimotor.data)

    if (cmd == 'A'):
      if (len(sur.message) == 5):
        # Sending the message that was received.
        print(sur.message)
        connection.send(sur.message)
        sur.message = ''

    elif (cmd == 'U'):
      # Activate/Deactivate sensor data.
      if (cmd_data == '!'):
        # IP Address exchange.
        sensorimotor.ip = address[0]
        sensorimotor.restart()

        print("Reloading target ip for telemetry:"+sensorimotor.ip)

      elif (cmd_data == 'Q'):
        sensesensor = True
      elif (cmd_data == 'q'):
        sensesensor = False

      elif (cmd_data == 'k'):
        reels.left(100)
      elif (cmd_data == 'l'):
        reels.right(100)

      elif (cmd_data == ' '):
        motors.stop()
        reels.stop()

      elif (cmd_data == 'w'):
        motors.both(100)
      elif (cmd_data == 's'):
        motors.both(-100)
      elif (cmd_data == 'd'):
        motors.left(100)
        motors.right(-100)
      elif (cmd_data == 'a'):
        motors.left(-100)
        motors.right(100)

      elif (cmd_data == 'X'):
        break

  except Exception as e:
    print("Error:" + str(e))
    print("Waiting for serial connection to reestablish...")
    connection.reconnect()

    # Instruct the Sensorimotor Cortex to stop wandering.
    sensorimotor.reset()

  sys.stdout.flush()  # for service to print logs

vst.keeprunning = False
vst.interrupt()
sur.keeprunning = False

# When everything done, release the capture
sock.close()
terminate()
