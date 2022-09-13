import serial
PORT = 'COM6'
DIVIDER = "|"
BAUDRATE = 19200

class SerialCommunicator:
    def __init__(self):
        self.arduino = serial.Serial(PORT, BAUDRATE)

    def write(self, msg):
        self.arduino.write(f'{msg}{DIVIDER}')