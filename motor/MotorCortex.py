import serial


class MotorCortex:
    def __init__(self, *, connection, speed = 120):
        # TODO: not used now. To be done
        self.connection = connection
        self.speed = speed

    def stop(self):
        self.connection.send(b'A3010')
        self.connection.send(b'A3000')
        self.connection.send(b'A0000')
        self.connection.send(b'A8000')
        self.connection.send(b'A7000')
        self.connection.send(b'P')

    def move_forward(self):
        self.connection.send(bytes('A3'+'{:3d}'.format(self.speed),'ascii'))

    def move_backwards(self):
        self.connection.send(bytes('A4'+'{:3d}'.format(self.speed),'ascii'))
    
    def move_left(self):
        self.connection.send(bytes('A1'+'{:3d}'.format(self.speed),'ascii'))

    def move_right(self):
        self.connection.send(bytes('A2'+'{:3d}'.format(self.speed),'ascii'))

    def increase_speed(self):
        self.speed = self.speed + 10
    
    def decrease_speed(self):
        self.speed = self.speed - 10