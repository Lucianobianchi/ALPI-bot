#coding: latin-1
import serial
import time
import datetime
from struct import *
import os

import socket
import sys

import Configuration


class SensorimotorCortex:
    def __init__(self, connection, name, length, mapping):
        self.connection = connection
        self.name = name
        self.keeprunning = True
        self.ip = Configuration.controllerip
        self.telemetryport = Configuration.telemetryport
        self.sensors = None
        self.data = None
        self.length = length
        self.mapping = mapping
        self.sensorlocalburst=1
        self.sensorburst=1
        self.updatefeq=1
        self.ztime = int(time.time())

    def start(self):
        # Sensor Recording
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        self.f = open('./data/sensor.'+self.name+'.'+st+'.dat', 'w')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.ip, self.telemetryport)
        self.counter = 0

    def init(self):
        # Clean buffer
        self.connection.read(1000)

        self.connection.send('AC'+'000')
        time.sleep(2)
        leng = self.connection.readsomething(2) # Reading INT

        datapack=unpack('h',leng)
        self.length = datapack[0]

        self.connection.send('AD'+'000')
        time.sleep(3)
        self.mapping = self.connection.gimmesomething()

    def stop(self):
        self.connection.send(b'A3010')
        self.connection.send(b'A3000')
        self.connection.send(b'A0000')


    def cleanbuffer(self):
        # Cancel sensor information.
        self.connection.send(b'X')
        time.sleep(6)

        # Ser should be configured in non-blocking mode.
        self.connection.read(1000)
        self.connection.flush()

        self.connection.send('AB'+'{:3d}'.format(self.sensorburst))
        self.connection.send('AE'+'{:3d}'.format(self.updatefreq))

        time.sleep(1)
        msg = self.connection.read(1000)
        print(msg)


    def log(self, mapping,data):
        new_values = unpack(mapping, data)
        ts = int(time.time())-self.ztime
        self.f.write(str(ts) + ' '+ ' '.join(map(str, new_values)) + '\n')

    def send(self,data):
        sent = self.sock.sendto(data, self.server_address)

    def repack(self,list_pos,list_values):
        new_values = unpack(self.mapping, self.data)
        new_values = list(new_values)

        # Update the structure with the values obtained from here.
        for i,x in enumerate(list_pos,0):
            new_values[x] = list_values[i]

        new_values = tuple(new_values)
        self.data = pack(self.mapping, *new_values)

    def picksensorsample(self):
        # read  Embed this in a loop.
        self.counter=self.counter+1
        if (self.counter>self.sensorlocalburst):
            self.connection.send('S')
            self.counter=0
        myByte = self.connection.read(1)
        if myByte == 'S':
          readcount = 0
          #data = readsomething(ser,44)
          self.data = self.connection.readsomething(self.length)
          myByte = self.connection.readsomething(1)
          if len(myByte) >= 1 and myByte == 'E':
              # is  a valid message struct
              #new_values = unpack('ffffffhhhhhhhhhh', data)
              new_values = unpack(self.mapping, self.data)
              print (new_values)
              self.sensors = new_values
              return new_values

        return None

    def close(self):
        self.f.close()
        self.sock.close()
        self.connection.close()

    def restart(self):
        self.close()
        self.start()

    def reset(self):
        self.connection.flush()
        self.cleanbuffer()
        self.send(b'AE010')
        self.send(b'AB100')


#sensorimotor = Sensorimotor('sensorimotor',66,'fffffffffffhhhhhhhhhhh')


