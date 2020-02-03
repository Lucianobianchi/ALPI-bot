import socket
import sys
from connection import Surrogator

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = sys.argv[1]
server_address = (ip, 30002)

sock.bind(server_address)
sur = Surrogator(sock)

while True:
  try:
    data = ''
    # TCP/IP server is configured as non-blocking
    sur.getmessage()

    cmd = sur.command
    cmd_data, address = sur.data, sur.address

    if cmd == 'S':
      print('Telemetry!!!')
  
  except Exception as err:
    print("An error has ocurred")
    print(err)