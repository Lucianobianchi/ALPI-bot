from connection.SerialConnection import SerialConnection
from telemetry.TelemetryLoader import TelemetryLoader
import time

serial = SerialConnection()
#serial.send(bytes('C00000', 'ascii'))
loader = TelemetryLoader(serial)
for i in range(100):
  time.sleep(5)
  print(loader.poll(frequency = 1, length = 1))