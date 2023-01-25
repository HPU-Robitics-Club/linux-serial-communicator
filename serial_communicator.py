import string
import serial
from enum import Enum

PORT = 'COM3'
DIVIDER = "|"
BAUDRATE = 9600

class SerialCommunicator:
    def __init__(self):
        self.arduino = serial.Serial(PORT, BAUDRATE)

    def write(self, msg: str):
        self.arduino.write(f'{msg}{DIVIDER}')
        print(f'{msg}{DIVIDER}')
    
    def write_motor_command(self, left_motor_code: str, right_motor_code: str, left_motor_value: int, right_motor_value: int):
        self.write(f'{left_motor_code}{left_motor_value}{right_motor_code}{right_motor_value}')

class MotorCode(Enum):
    WHEELS_FORWARD = "wf"
    WHEELS_BACKWARD = "wb"