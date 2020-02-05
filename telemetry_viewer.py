import os
import fcntl
import errno
import json
import socket
from connection import Surrogator
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from control import distances, follow_turn, rotate_go
from time import sleep

red_color = 'tab:red'
blue_color = 'tab:blue'

fig, [(l_reel_axes, r_reel_axes), (ft_v_axes, rg_v_axes)] = plt.subplots(2, 2)

l_thread_axes, r_thread_axes = l_reel_axes.twinx(), r_reel_axes.twinx()

l_reel_axes.set_ylabel('Pulses')
l_reel_axes.set_title('Left Reel')
l_reel_axes.tick_params(axis='y', labelcolor=blue_color)

r_reel_axes.set_ylabel('Pulses')
r_reel_axes.set_ylabel('Right Reel')
r_reel_axes.tick_params(axis='y', labelcolor=blue_color)

l_thread_axes.set_ylabel('Length [m]')
l_thread_axes.tick_params(axis='y', labelcolor=red_color)

r_thread_axes.set_ylabel('Length [m]')
r_thread_axes.tick_params(axis='y', labelcolor=red_color)

ft_v_axes.set_ylabel('Wheel power [0 - 255]')
ft_v_axes.set_title('Wheel speeds (F&T)')
(left_ft_bar, right_ft_bar) = ft_v_axes.bar(['left', 'right'], [0, 0])

rg_v_axes.set_ylabel('Wheel power [-255 - 255]')
rg_v_axes.set_title('Wheel speeds (R&G)')
(left_rg_bar, right_rg_bar) = rg_v_axes.bar(['left', 'right'], [0, 0])

l_reel_line, = l_reel_axes.plot([0], [0], color=blue_color)
r_reel_line, = r_reel_axes.plot([0], [0], color=blue_color)
l_thread_line, = l_thread_axes.plot([0], [0], color=red_color)
r_thread_line, = r_thread_axes.plot([0], [0], color=red_color)

sensor_datas = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_address = ('', 30002)
sock.bind(server_address)

fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)

sur = Surrogator(sock)

all_shapes = [l_reel_line, r_reel_line, l_thread_line,
              r_thread_line, left_ft_bar, right_ft_bar, left_rg_bar, right_rg_bar]

def init():
  l_reel_axes.set_xlim(0, 25)
  l_reel_axes.set_ylim(-300, 300)
  r_reel_axes.set_xlim(0, 25)
  r_reel_axes.set_ylim(-300, 300)
  l_thread_axes.set_xlim(0, 25)
  l_thread_axes.set_ylim(-1, 1)
  r_thread_axes.set_xlim(0, 25)
  r_thread_axes.set_ylim(-1, 1)
  ft_v_axes.set_ylim(0, 255)
  rg_v_axes.set_ylim(-255, 255)
  return all_shapes


def update(i):
  try:
    message, address = sock.recvfrom(10000)
    if message != '' and message[0] != 'T':
      data = json.loads(message[1:])
      sensor_datas.append(data[0])
      # print(data[0])

  except Exception as exc:
    err = exc.args[0]
    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
      pass # no data available
    else:
      print("An error has ocurred")
      print(exc)

  finally:
    data_len = len(sensor_datas)
    if data_len > 15:
      graph_data = sensor_datas[-15:]
    else:
      graph_data = sensor_datas

    if data_len > 0:
      x_range = range(len(graph_data))

      l_encs = map(lambda d: d['leftReelEncoder'], graph_data)
      r_encs = map(lambda d: d['rightReelEncoder'], graph_data)
      l_reel_line.set_data(x_range, list(l_encs))
      r_reel_line.set_data(x_range, list(r_encs))

      dists = list(map(distances, graph_data))
      l_thread_line.set_data(x_range, [ld for ld, rd in dists])
      r_thread_line.set_data(x_range, [rd for ld, rd in dists])

      ft_lv, ft_rv = follow_turn([graph_data[-1]])
      rg_lv, rg_rv = rotate_go([graph_data[-1]])
      left_ft_bar.set_height(ft_lv)
      right_ft_bar.set_height(ft_rv)
      left_rg_bar.set_height(rg_lv)
      right_rg_bar.set_height(rg_rv)

    return all_shapes


ani = animation.FuncAnimation(
    fig, update, None, init_func=init, interval=30, blit=True)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
