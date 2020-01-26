from struct import unpack

# From Arduino code
# struct {
#   long code; + 4
#   long rightEncoder; + 4 // 8
#   long leftEncoder; + 4 // 12
#   long rightReelEncoder; + 4 // 16
#   long leftReelEncoder; + 4 // 20
#   float voltage; + 4 // 24
#   float current; + 4 // 28
#   long freq; + 4 // 32
#   long counter; + 4 // 36
# }

UNPACK_FMT = 'iiiiiffii'

TELEMETRY_KEYS = [
  'code', 'rightWheelEncoder', 'leftWheelEncoder',
  'rightReelEncoder', 'leftReelEncoder', 'voltage',
  'current', 'frequency', 'counter'
]

PAYLOAD_SIZE = 36

class TelemetryLoader:
  def __init__(self, serial_connection):
    self.serial_connection = serial_connection

  def poll(self, *, frequency, length):
    # Set frequency
    self.serial_connection.send(bytes('S1B'+'{:3d}'.format(frequency), 'ascii'))

    # Start sensor burst
    self.serial_connection.send(bytes('S01'+'{:3d}'.format(length), 'ascii'))

    res = []
    for _ in range(length):
      start = self.serial_connection.read(1)
      payload = self.serial_connection.read(PAYLOAD_SIZE)
      end = self.serial_connection.read(1)
      if start == b'{' and end == b'}' and len(payload) == PAYLOAD_SIZE:
        # Valid payload
        values = unpack(UNPACK_FMT, payload)
        data = {k: values[i] for (i, k) in enumerate(TELEMETRY_KEYS)}
        res.append(data)
      else:
        # TODO: throw exception so that the calling function has to catch it in case 
        # the serial connection doesn't work
        print('Skipped invalid payload')

    return res
  
  def stop(self):
    self.serial_connection.send(bytes('S02000', 'ascii'))

  def payload_size(self):
    self.serial_connection.send(bytes('S21000', 'ascii'))
    payload = self.serial_connection.read(2)
    size = unpack('s', payload)
    return size[0]