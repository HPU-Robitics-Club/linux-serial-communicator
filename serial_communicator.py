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
    
    def write_motor_command(self, motor_code: str, left_motor_value: int, right_motor_value: int):
        self.write(f'{motor_code}{left_motor_value}{right_motor_value}')

class MotorCode(Enum):
    WHEELS = "w"