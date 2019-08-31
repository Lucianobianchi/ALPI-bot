import time
import serial
import datetime

TRIES = 10

class SerialConnection(object): 
  def __init__(self, *, portname):
    self.open = False
    tries = 0
    while (tries < TRIES):
      try:
        print(f"Opening port {portname}. Try {tries + 1}...")
        self.serial_port = serial.Serial(port = portname, timeout=0)
        self.open = True
        print(f"Opened port {self.serial_port}")
        break
      except: 
        tries += 1
    
    if (not self.open):
      print('Could not open serial port. Mocking serial...')

  def send(self, bytes):
    if (self.open):
      print(f"Sending via serial: {bytes}")
      self.serial_port.write(bytes)
    else:
      print('Warning: serial port not open.')

  def read(self, bytes):
    pass    