class SerialReel:
  def __init__(self, *, connection):
    self.connection = connection

  # TODO: check speed > 0
  def left(self, speed):
    self.connection.send(bytes('A0A'+'{:3d}'.format(speed), 'ascii'))

  def right(self, speed):
    self.connection.send(bytes('A0B'+'{:3d}'.format(speed), 'ascii'))

  def both(self, speed):
    self.connection.send(bytes('A0C'+'{:3d}'.format(speed), 'ascii'))

  def stop(self):
    self.connection.send(bytes('A0D000', 'ascii'))
