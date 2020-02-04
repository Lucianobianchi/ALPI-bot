# coding: latin-1
import socket
import sys
import time
from connection import MCast
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = sys.argv[1]
print("Using IP:"+ip)

server_address = (ip, 30001)

def _find_getch():
  try:
    import termios
  except ImportError:
    # Non-POSIX. Return msvcrt's (Windows') getch.
    import msvcrt
    return msvcrt.getch

  # POSIX system. Create and return a getch that manipulates the tty.
  import tty

  def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

  return _getch


getch = _find_getch()

print('Press X to stop Bot')
print('Press x to exit this controller')
print('Press f to enter new update frequency for the bot.')

while (True):
  print('>')
  data = getch()

  if (data.startswith('x')):
    sock.close()
    quit()

  sent = sock.sendto(bytes('U'+data+'000', 'ascii'), server_address)

  if (data.startswith('!')):
    print("Letting know Bot that I want streaming....")

  if (data.startswith('X')):
    break

print("Stopping ALPIBot....")
for i in range(1, 100):
  sent = sock.sendto(bytes('U'+data+'000', 'ascii'), server_address)

sock.close()
