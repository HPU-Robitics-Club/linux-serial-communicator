import string
import serial
from enum import Enum

PORT = 'COM6'
DIVIDER = "|"
BAUDRATE = 19200

class SerialCommunicator:
    def __init__(self):
        self.arduino = serial.Serial(PORT, BAUDRATE)

    def write(self, msg: str):
        self.arduino.write(f'{msg}{DIVIDER}')
    
    def write_motor_command(self, motor_code: str, motor_value: int):
        self.write(f'{motor_code}{motor_value}')

class MotorCode(Enum):
    RIGHT = "rw"
    LEFT = "lw"
    ALL = "aw"