import string
import serial
from enum import Enum

PORT = 'COM3'
DIVIDER = "|"
BAUDRATE = 9600

class SerialCommunicator:
    def __init__(self):
        self.arduino = serial.Serial(PORT, BAUDRATE)
        print("Starting serial communicator...")

    def write(self, msg: str):
        self.arduino.write(f'{msg}{DIVIDER}')
        print(f'{msg}{DIVIDER}')
    
    def write_motor_command(self, left_motor_code: str, right_motor_code: str, left_motor_value: int, right_motor_value: int):
        self.write(f'{left_motor_code}{self.format_motor_value(left_motor_value)}{right_motor_code}{self.format_motor_value(right_motor_value)}')

    def format_motor_value(self, motor_value: int):
        N = 0
        if motor_value < 10:
            N = 2
        elif motor_value < 100:
            N = 1
        
        output_str = str(motor_value)
        for i in range(0, N):
            output_str = f'0{output_str}'

        return output_str

class MotorCode():
    WHEELS_FORWARD = "wf"
    WHEELS_BACKWARD = "wb"