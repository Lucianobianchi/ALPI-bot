#coding: latin-1

# NeoCortex is the core program to control ShinkeyBot
# It handles basic USB-Serial comm with other modules and handles
# the basic operation of ShinkeyBot
#
# x) Transmit TCP/IP images through CameraStreamer.
# x) Captures sensor data from SensorimotorLogger
# x) Handles output to motor unit and sensorimotor commands through Proprioceptive
# x) Receives high-level commands from ShinkeyBotController.

import numpy as np
import cv2

import serial

import time
import datetime
from struct import *

import sys, os, select

import socket

import Proprioceptive as prop
import thread
#import PicameraStreamer as pcs
import SensorimotorLogger as senso
import MCast

import fcntl
import struct

from Fps import Fps

import MotorBridge
import time

motor = MotorBridge.MotorBridgeCape()
motor.DCMotorInit(1,1000)
motor.DCMotorInit(2,1000)
motor.DCMotorInit(3,1000)
motor.DCMotorInit(4,1000)

# First create a witness token to guarantee only one instance running
if (os.access("running.wt", os.R_OK)):
    print >> sys.stderr, 'Another instance is running. Cancelling.'
    quit(1)

runningtoken = open('running.wt', 'w')
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

runningtoken.write(st)
runningtoken.close()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


# Get PiCamera stream and read everything in another thread.
#vst = pcs.H264VideoStreamer()
#try:
#    vst.startAndConnect()
#    pass
#except:
#    pass

# Ok, so the first thing to do is to broadcast my own IP address.
dobroadcastip = True

# Initialize UDP Controller Server on port 10001 (ShinkeyBotController)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 10001)
print >> sys.stderr, 'Starting up Controller Server on %s port %s', server_address
sock.bind(server_address)

if (dobroadcastip):
    sock.setblocking(0)
    sock.settimeout(0.01)

noticer = MCast.Sender()

# Fixme push the network name inside the configuration file.
myip = get_ip_address('wlan0')

if (len(myip)>0):
    myip = myip
else:
    myip = 'None'

# Shinkeybot truly does nothing until it gets connected to ShinkeyBotController
whenistarted = time.time()
print 'Multicasting my own IP address:' + myip
while dobroadcastip:
    noticer.send()
    try:
        data, address = sock.recvfrom(1)
        if (len(data)>0):
            break
    except:
        data = None

    if (abs(time.time()-whenistarted)>60):
        print 'Giving up broadcasting ip... Lets get started.'
        break

from threading import Timer

def timeout():
    print 'Sending a multicast update of my own ip address:'+myip
    noticer.send()

t = Timer(5 * 60, timeout)
t.start()

if (dobroadcastip):
    sock.setblocking(1)
    sock.settimeout(0)

print 'Connection to Remote Controller established.'

# Open connection to tilt sensor (@deprecated)
#hidraw = prop.setupsensor()
# Open serial connection to MotorUnit and Sensorimotor Arduinos.
def doserial():
    retries=1
    ssmr=None
    mtrn=None
    while (retries<5):
        try:
            [ssmr, mtrn] = prop.serialcomm()
            print 'Connection established'
            return [ssmr, mtrn]
        except Exception as e:
            print 'Error while establishing serial connection.'
            retries=retries+1

    return [ssmr, mtrn]

#[ssmr, mtrn] = doserial()

ssmr = None
mtrn = None


def stopMotors():
    motor.DCMotorStop(1)
    motor.DCMotorStop(2)
    motor.DCMotorStop(3)
    motor.DCMotorStop(4)


def terminateme():
    try:
        t.cancel()
        motor.DCMotorStop(1)
        motor.DCMotorStop(2)
        motor.DCMotorStop(3)
        motor.DCMotorStop(4)
        print 'Thread successfully closed.'
    except Exception as e:
        print 'Exception while closing video stream thread.'
        traceback.print_exc(file=sys.stdout)

    os.remove('running.wt')
    print 'ShinkeyBot has stopped.'


#if (ssmr == None and mtrn == None):
#    terminateme()

# Instruct the Sensorimotor Cortex to stop wandering.
#ssmr.write('C')

tgt = -300

wristpos=90
elbowpos = 90
shoulderpos = 150

# Pan and tilt
visualpos = [90,95]

scan = 90

pwmduty = 190

# Enables the sensor telemetry.  Arduinos will send telemetry data that will be
#  sent to listening servers.
sensesensor = False

# Connect remotely to any client that is waiting for sensor loggers.
# sensorimotor = senso.Sensorimotor('sensorimotor',52,'ffffffhhhhhhhhhhhhhh')
# sensorimotor.start()
# sensorimotor.cleanbuffer(ssmr)
#
# if (mtrn):
#     motorneuron = senso.Sensorimotor('motorneuron',26,'hhffffhhh')
#     motorneuron.start()
#     motorneuron.cleanbuffer(mtrn)


class Surrogator:
    def __init__(self, sock):
        print 'Remote controlling ShinkeyBot'
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
        except Exception as e:
            pass

    def getmessage(self):
        self.data = ''
        try:
            # Read from the UDP controller socket non blocking
            # The message format is AANNN
            self.message, self.address = self.sock.recvfrom(5)
            self.command = self.message[0]
            self.data = self.message[1]
            self.controlvalue = int(self.message[2:5])
        except Exception as e:
            pass


    def hookme(self):
        while (self.keeprunning):
            nextdata  = ''
            self.getcommand()

            if (self.data == 'X'):
                break

        print 'Stopping surrogate...'

sur = Surrogator(sock)

#try:
#    thread.start_new_thread( sur.hookme, () )
#    pass
#except:
#    pass

target = [0,0,0]
automode = False;

fps = Fps()
fps.tic()

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
runninglog = open('../data/brainstem.'+st+'.dat', 'w')

# Live
while(True):
    try:
        fps.steptoc()
        ts = int(time.time())
        runninglog.write(str(ts) + ',' + str(fps.fps) + '\n')
        #print "Estimated frames per second: {0}".format(fps.fps)
        data = ''
        # TCP/IP server is configured as non-blocking
        sur.getmessage()
        data, address = sur.data, sur.address

        # If someone asked for it, send sensor information.
        if (sensesensor):
            sens = sensorimotor.picksensorsample(ssmr)
            mots = None

            if (mtrn):
                mots = motorneuron.picksensorsample(mtrn)

            if (sens != None and mots != None):
                sensorimotor.send(sensorimotor.data+motorneuron.data)

            if (sens != None):
                sensorimotor.send(sensorimotor.data)

            if (sens != None and target != None):
                if (target[0] == 0):
                    target = sens[9], sens[10], sens[11]

                if (automode):
                    #print "Moving to :" + str(target[0]) + '\t' + str(target[1]) + '\t' + str(target[2])
                    #print "From:     :" + str(sens[9])   + '\t' + str(sens[10])  + '\t' + str(sens[11])
                    #if (not ( abs(sens[9]-target[0])<10) ):
                    #    ssmr.write('-')
                    #    ssmr.write('4')
                    #    time.sleep(0.2)
                    #    ssmr.write('5')
                    #    time.sleep(0.1)

                    print 'Auto:Sensing distance:'+str(sens[15])
                    ssmr.write('+')
                    ssmr.write('2')
                    if (sens[15]<90):
                        ssmr.write('5')
        if (sur.command == 'A'):
            if (len(sur.message)==5):
                # Sending the message that was received.
                ssmr.write(sur.message)
                sur.message = ''

        elif (sur.command == 'U'):

            if (data == '!'):
                # IP Address exchange.
                sensorimotor.ip = address[0]
                sensorimotor.restart()

                if (mtrn):
                    motorneuron.ip = address[0]
                    motorneuron.restart()

                print "Reloading target ip for telemetry:"+sensorimotor.ip

                # Vst VideoStream should be likely restarted in order to check
                # if something else can be enabled.


            if (data == 'Q'):
                # Activate/Deactivate sensor data.
                sensesensor = True
            elif (data == 'q'):
                sensesensor = False

            if (data == '='):
                #Home position.
                mtrn.write('=')
                wristpos=90
                elbowpos=90
                shoulderpos=150
                mtrn.write('AC000')
                # wrist down
            elif (data==' '):
                stopMotors()
                # Quiet
            elif (data=='W'):
                motor.DCMotorMove(1,1,pwmduty)
                motor.DCMotorMove(2,1,pwmduty)
                motor.DCMotorMove(3,1,pwmduty)
                motor.DCMotorMove(4,1,pwmduty)
                # Forward
            elif (data=='S'):
                motor.DCMotorMove(1,2,pwmduty)
                motor.DCMotorMove(2,2,pwmduty)
                motor.DCMotorMove(3,2,pwmduty)
                motor.DCMotorMove(4,2,pwmduty)
                # Backward
            elif (data=='D'):
                motor.DCMotorMove(1,1,pwmduty)
                motor.DCMotorMove(2,2,pwmduty)
                motor.DCMotorMove(3,1,pwmduty)
                motor.DCMotorMove(4,2,pwmduty)
                # Right
            elif (data=='A'):
                motor.DCMotorMove(1,2,pwmduty)
                motor.DCMotorMove(2,1,pwmduty)
                motor.DCMotorMove(3,2,pwmduty)
                motor.DCMotorMove(4,1,pwmduty)
                # Left
            elif (data=='K'):
                motor.DCMotorMove(1,2,pwmduty)
                motor.DCMotorMove(2,1,pwmduty)
                motor.DCMotorMove(3,1,pwmduty)
                motor.DCMotorMove(4,2,pwmduty)
                # Rotate Left
            elif (data=='L'):
                motor.DCMotorMove(1,1,pwmduty)
                motor.DCMotorMove(2,2,pwmduty)
                motor.DCMotorMove(3,2,pwmduty)
                motor.DCMotorMove(4,1,pwmduty)
                # Rotate Right
            elif (data=='.'):
                pwmduty = pwmduty - 10
                # Move slowly
            elif (data==','):
                pwmduty = pwmduty + 10
                # Move coarsely


            elif (data=='('):
                sensorimotor.sensorlocalburst = 100
            elif (data==')'):
                sensorimotor.sensorlocalburst = 10000
            elif (data=='X'):
                break
    except Exception as e:
        print "Error:" + e.message
        print "Waiting for serial connection to reestablish..."
        if (not ssmr == None):
            ssmr.close()
        if (not mtrn == None):
            mtrn.close()
        #[ssmr, mtrn] = doserial()

        # Instruct the Sensorimotor Cortex to stop wandering.
        if (ssmr != None):
            ssmr.write('C')

#vst.keeprunning = False
sur.keeprunning = False
time.sleep(2)


#When everything done, release the capture
if (not ssmr == None):
    ssmr.close()
sock.close()
if (not mtrn == None):
    mtrn.close()

terminateme()
