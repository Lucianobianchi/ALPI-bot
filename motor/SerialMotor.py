class SerialMotor:
  def __init__(self, *, connection):
    self.connection = connection

  # TODO: check speed range
  def left(self, speed):
    if speed >= 0:  # Forward
      self.connection.send(bytes('A01'+'{:3d}'.format(speed), 'ascii'))
    else:  # Backwards
      self.connection.send(bytes('A03'+'{:3d}'.format(abs(speed)), 'ascii'))

  def right(self, speed):
    if speed >= 0:  # Forward
      self.connection.send(bytes('A02'+'{:3d}'.format(speed), 'ascii'))
    else:  # Backwards
      self.connection.send(bytes('A04'+'{:3d}'.format(abs(speed)), 'ascii'))

  def both(self, speed):
    if speed >= 0:  # Forward
      self.connection.send(bytes('A05'+'{:3d}'.format(speed), 'ascii'))
    else:  # Backwards
      self.connection.send(bytes('A06'+'{:3d}'.format(abs(speed)), 'ascii'))

  def stop(self):
    self.connection.send(bytes('A07000', 'ascii'))
