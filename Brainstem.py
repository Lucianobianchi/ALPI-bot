import Configuration
import serial
import time
import datetime
from struct import *
import struct
import sys, os, select
import socket
import fcntl
from threading import Timer
import signal
import time

from connection import MCast
from motor.SerialMotorController import SerialMotorController
from SerialConnection import SerialConnection

# First create a witness token to guarantee only one instance running
if (os.access("running.wt", os.R_OK)):
    print('Another instance is running. Cancelling.')
    quit(1)

runningtoken = open('running.wt', 'w')
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

runningtoken.write(st)
runningtoken.close()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Initialize UDP Controller Server on port 10001 (BotController)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 10001)
print(f"Starting up Controller Server on {server_address[0]} port {server_address[1]}")
sock.bind(server_address)

if (Configuration.broadcast_IP):
    sock.setblocking(0)
    sock.settimeout(0.01)

noticer = MCast.Sender()

# Fixme push the network name inside the configuration file.
myip = get_ip_address('wlan0')

if (len(myip)>0):
    myip = myip
else:
    myip = 'None'

start = time.time()
print('Multicasting my own IP address: ' + myip)
while Configuration.broadcast_IP:
    noticer.send()
    try:
        data, address = sock.recvfrom(1)
        if (len(data) > 0):
            break
    except:
        data = None

    if (abs(time.time()- start) > 5):
        print('Giving up broadcasting ip... Lets get started.')
        break

def timeout():
    print ('Sending a multicast update of my own ip address:'+myip)
    noticer.send()

if (Configuration.broadcast_IP):
    sock.setblocking(1)
    sock.settimeout(0)

def terminate():
    try:
        motor.stop()
        print('Motors successfully stopped.')
    except e:
        print('Exception while stopping motors.', e)
    finally:
        os.remove('running.wt')
    print ('ALPIBot has stopped.')

signal.signal(signal.SIGINT, terminate)

tgt = -300

# Enables the sensor telemetry.  Arduinos will send telemetry data that will be
#  sent to listening servers.
sensesensor = False

class Surrogator:
    def __init__(self, sock):
        print ('Remote controlling ALPIBot')
        self.data = ''
        self.message = ''
        self.controlvalue = 0
        self.command = ''
        self.sock = sock
        self.address = None
        self.keeprunning = True

    def getdata(self):
        return self.data

    def getcommand(self):
        self.data = ''
        try:
            # Read from the UDP controller socket non blocking
            self.data, self.address = self.sock.recvfrom(1)
        except Exception:
            pass

    def getmessage(self):
        self.data = ''
        self.command = ''
        try:
            # Read from the UDP controller socket non blocking
            # The message format is AANNN
            self.message, self.address = self.sock.recvfrom(5)
            self.command = chr(int(self.message[0]))
            self.data = chr(int(self.message[1]))
            print('Data', self.data)
            self.controlvalue = int(self.message[2:5])
        except Exception:
            pass


    def hookme(self):
        while (self.keeprunning):
            nextdata  = ''
            self.getcommand()

            if (self.data == 'X'):
                break

        print ('Stopping surrogate...')

sur = Surrogator(sock)

target = [0,0,0]

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

connection = SerialConnection(portname='/dev/ttys000')
motor = SerialMotorController(connection = connection)

# Live
while(True):
        # TCP/IP server is configured as non-blocking
    sur.getmessage()
    
    cmd = sur.command
    cmd_data = sur.data

    if (cmd_data != ''):
        print(cmd)
        print(cmd_data)

    if (cmd == 'A'):
        if (len(sur.message)==5):
            # Sending the message that was received.
            # ssmr.write(sur.message)
            sur.message = ''

    elif (cmd == 'U'):
        # Activate/Deactivate sensor data.
        if (cmd_data == 'Q'):
            sensesensor = True
        elif (cmd_data == 'q'):
            sensesensor = False

        elif (cmd_data == ' '):
            motor.stop()
        elif (cmd_data == 'w'):
            motor.move_forward()
        elif (cmd_data == 's'):
            motor.move_backwards()
        elif (cmd_data == 'd'):
            motor.move_right()
        elif (cmd_data == 'a'):
            motor.move_left()
        elif (cmd_data == 'k'):
            motor.rotate_left()
        elif (cmd_data == 'l'):
            motor.rotate_right()
        elif (cmd_data == '.'):
            motor.decrease_speed()
        elif (cmd_data == ','):
            motor.increase_speed()
        elif (cmd_data == 'X'):
            break

sur.keeprunning = False
time.sleep(2)

#When everything done, release the capture
sock.close()
