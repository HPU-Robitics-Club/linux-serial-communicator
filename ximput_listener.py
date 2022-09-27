import math
from turtle import left
from serial_communicator import MotorCode, SerialCommunicator
import xbox

def registerXinputListener(serial: SerialCommunicator):
    joy = xbox.Joystick()
    xinputListener(joy, serial)

def xinputListener(joy, serial: SerialCommunicator):
    while True:
        if (joy.A()):
            serial.write_motor_command(MotorCode.WHEELS, 0, 0)
        elif (joy.leftTrigger() > 0):
            leftTrigger = joy.leftTrigger()

            magSpeed = int(leftTrigger * 255)
            serial.write_motor_command(MotorCode.WHEELS, -magSpeed, magSpeed)
        elif (joy.rightTrigger() > 0):
            rightTrigger = joy.rightTrigger()

            magSpeed = int(rightTrigger * 255)
            serial.write_motor_command(MotorCode.WHEELS, magSpeed, -magSpeed)
        else:
            x, y = joy.leftStick()

            leftSpeed = 0
            rightSpeed = 0

            # Evaluate y component and speed
            magSpeed = int(y * 255)
            leftSpeed = magSpeed
            rightSpeed = magSpeed

            # Evaluate x component and turning
            if (x != 0):
                magTurnDiff = int(x * 127)
                if (magTurnDiff > 0):
                    leftSpeed -= magTurnDiff
                else:
                    rightSpeed -= magTurnDiff

            serial.write_motor_command(MotorCode.WHEELS, leftSpeed, rightSpeed)

def xboxControl(self):
    joy = xbox.Joystick()
    while True:
    
        
        # button A to stop
        if joy.A():
            self.motor.stop()
        else:
            # left joystick to move
            x, y = joy.leftStick()
            self.moveByAxis(x, y)
            # left trigger hard left
            trigger = joy.leftTrigger()
            # right trigger hard right
            trigger = joy.rightTrigger()    
    joy.close()