import platform
import time
import serial
import datetime
import os

import datetime

baudrate = 9600

TRIES = 10

system_platform = platform.system()
if system_platform == "Darwin":
  import FFMPegStreamer as pcs
  portname = '/dev/cu.usbmodem14101'
else:
  import H264Streamer as pcs
  portname = None


class SerialConnection(object):
  def __init__(self):
    self.connect()

  def connect(self):
    self.open = False
    for t in range(0, TRIES):
      try:
        self.ser = self.serialcomm(timeout = 1)
        self.open = True
        print('Opened port ' + str(self.ser))

        # Cleanup
        self.read(100000)

        print('Connected to ALPIBot Arduino module')

        break
      except Exception as e:
        print('Error while establishing serial connection:' + str(e))

  def serialcomm(self, timeout):
      # Mac
    if system_platform == "Darwin":
      print('Mac environment. Trying port /dev/cu.usbmodem14101...')
      ser = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=baudrate, timeout=timeout)
    # Raspberry
    else:
      print('Raspi environment. Trying ports /dev/ttyACM...')
      for p in range(0, 16):
        port = '/dev/ttyACM' + str(p)
        if (os.path.exists(port)):
          ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
          break
        time.sleep(5)
    return ser

  def send(self, data):
    if self.open:
      self.ser.write(data)
    else:
      print('Warning: serial port not open.')

  def read(self, length):
    if self.open:
      return self.ser.read(length)
    else:
      print('Warning: serial port not open.')
      return None

  # There could be a chance that whatever is behind the serial connection get stuck
  # and do not reply anything.  Hence I need a way to break this up (that is what trials is for)
  def readsomething(self, length):
    data = b''
    trials = 10000000

    while(len(data) < length and trials > 0):
      byte = self.ser.read(1)
      # print(byte)
      trials = trials - 1
      if (len(byte) > 0):
        data = b''.join([data, byte])

    return data

  def flush(self):
    self.ser.flush()
    self.ser.flushInput()
    self.ser.flushOutput()

  def close(self):
    if (not self.ser == None):
      self.ser.close()

  def reconnect(self):
    self.flush()
    self.close()
    self.connect()
