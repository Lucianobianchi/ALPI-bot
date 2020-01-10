class Surrogator:
    def __init__(self, sock):
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
        except Exception:
            pass

    def getmessage(self):
        self.data = ''
        self.command = ''
        try:
            # Read from the UDP controller socket non blocking
            # The message format is AANNN
            self.message, self.address = self.sock.recvfrom(5)
            self.command = chr(int(self.message[0]))
            self.data = chr(int(self.message[1]))
            self.controlvalue = int(self.message[2:5])
        except Exception:
            pass

    def hookme(self):
        while (self.keeprunning):
            nextdata  = ''
            self.getcommand()

            if (self.data == 'X'):
                break

        print ('Stopping surrogate...')