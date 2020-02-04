import os
import fcntl
import errno
import json
import socket
from connection import Surrogator
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from control import distances
from time import sleep

fig, [(l_reel_axes, r_reel_axes), (l_thread_axes, r_thread_axes), (v_axes, _)] = plt.subplots(3,2)

# l_reel_axes = fig.add_subplot(3, 2, 1)
l_reel_axes.set_ylabel('Pulses')
l_reel_axes.set_title('Left Reel Encoder')

# r_reel_axes = plt.subplot(3, 2, 2)
r_reel_axes.set_ylabel('Pulses')
r_reel_axes.set_title('Right Reel Encoder')

# l_thread_axes = plt.subplot(3, 2, 3)
l_thread_axes.set_ylabel('Length [mm]')
l_thread_axes.set_title('Left Thread Length Difference')

# r_thread_axes = plt.subplot(3, 2, 4)
r_thread_axes.set_ylabel('Length [m]')
r_thread_axes.set_title('Right Thread Length Difference')

l_thread_axes.set_ylim(-0.5, 0.5)
r_thread_axes.set_ylim(-0.5, 0.5)

# v_axes = plt.subplot(3, 2, 5)
v_axes.set_ylabel('Wheel power [0-255]')
v_axes.set_title('Calculated wheel velocities')

v_axes.set_ylim(100, 256)

l_reel_line, = l_reel_axes.plot([0], [0])
r_reel_line, = r_reel_axes.plot([0], [0])

lr_enc_data = [0]
rr_enc_data = [0]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_address = ('', 30002)
sock.bind(server_address)

fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)

sur = Surrogator(sock)
print('Running!')
print(l_reel_line, r_reel_line)

def init():
  l_reel_axes.set_xlim(0, 20)
  r_reel_axes.set_xlim(0, 20)
  l_reel_axes.set_ylim(-50, 50)
  r_reel_axes.set_ylim(-50, 50)
  return l_reel_line, r_reel_line

def update(i):
  try:
    message, address = sock.recvfrom(10000)
    if message != '' and message[0] != 'T':
      data = json.loads(message[1:])
      lr_enc_data.append(data[0]['leftReelEncoder'])
      rr_enc_data.append(data[0]['rightReelEncoder'])
      print(data)

  except Exception as exc:
    err = exc.args[0]
    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
      # sleep(1)  # No data available
      pass
    else:
      print("An error has ocurred")
      print(exc)
  
  finally:  
    l_reel_line.set_data(range(len(lr_enc_data)), lr_enc_data)
    r_reel_line.set_data(range(len(rr_enc_data)), rr_enc_data)
    # print(lr_enc_data)
    # print(rr_enc_data)
    return l_reel_line, r_reel_line
  
ani = animation.FuncAnimation(fig, update, None, init_func=init, interval=1000, blit=True)
plt.show()
