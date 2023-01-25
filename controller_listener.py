from turtle import left
from serial_communicator import MotorCode, SerialCommunicator
import pygame

def registerControllerListener(serial: SerialCommunicator):
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
    controllerListener(serial, controller)

def controllerListener(serial: SerialCommunicator, controller):
    controller.get_numbuttons()
    controller.get_numhats()
    x = 0
    y = 0
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.JOYBUTTONDOWN and event.button == 1):
                serial.write_motor_command(MotorCode.WHEELS_FORWARD, MotorCode.WHEELS_FORWARD, 0, 0)
            elif (event.type == pygame.JOYAXISMOTION):
                if (event.axis == 4):
                    # left trigger
                    mag = event.value
                    rightSpeed = mag * 255
                    leftSpeed = -mag * 255
                    parseAndSendMotorCode(leftSpeed, rightSpeed, serial)
                elif (event.axis == 5):
                    # right trigger
                    mag = event.value
                    rightSpeed = -mag * 255
                    leftSpeed = mag * 255
                    parseAndSendMotorCode(leftSpeed, rightSpeed, serial)
                elif (event.axis == 2 or event.axis == 3):
                    # x controller
                    if (event.axis == 2):
                        if (event.value != 0):
                            x = event.value
                        
                    # y component
                    elif (event.axis == 3):
                        if (event.value != 0):
                            y = event.value
                        

                    if (x is not None and y is not None):
                        # print(f'x = {x}')
                        # print(f'y = {y}')
                        ySine = -abs(y)/y if y != 0 else 1
                        xSine = abs(x)/x if x != 0 else 1
                        
                        leftSpeed = 0
                        rightSpeed = 0
                        if abs(x) > 0.1 or abs(y) > 0.1:
                            if abs(x) <= 0.5:
                                leftSpeed = -y * 127 + ySine * 128
                                rightSpeed = leftSpeed
                            else:
                                leftSpeed = x * 127 + xSine * 128
                                rightSpeed = -leftSpeed

                        '''
                        leftSpeed = 0
                        rightSpeed = 0
                        if (y != 0):
                            magSpeed = -int(y * 255)
                            leftSpeed = magSpeed
                            rightSpeed = magSpeed
                            print(f'leftSpeed = {leftSpeed}, rightSpeed = {rightSpeed}')

                        if (x != 0):
                            magTurnDiff = abs(int(x * 127))
                            if (x > 0):
                                if (leftSpeed < 0):
                                    if (rightSpeed + magTurnDiff > 0):
                                        leftSpeed -= magTurnDiff
                                    else:
                                        rightSpeed += magTurnDiff
                                else:
                                    if (leftSpeed - magTurnDiff < 0):
                                        leftSpeed += magTurnDiff
                                    else: 
                                        rightSpeed -= magTurnDiff
                            else:
                                if (rightSpeed < 0):
                                    if (leftSpeed + magTurnDiff > 0):
                                        rightSpeed -= magTurnDiff
                                    else:
                                        leftSpeed += magTurnDiff
                                else:
                                    if (rightSpeed - magTurnDiff < 0):
                                        rightSpeed += magTurnDiff
                                    else:
                                        leftSpeed -= magTurnDiff
                        '''

                        parseAndSendMotorCode(leftSpeed, rightSpeed, serial)

def parseAndSendMotorCode(leftSpeed: int, rightSpeed: int, serial):
    leftSpeed = round(leftSpeed) if abs(leftSpeed) > 30 else 0
    rightSpeed = round(rightSpeed) if abs(rightSpeed) > 30 else 0
    # print(f'leftSpeed = {leftSpeed}, rightSpeed = {rightSpeed}')
    left_motor_code = MotorCode.WHEELS_FORWARD if leftSpeed >= 0 else MotorCode.WHEELS_BACKWORD
    right_motor_code = MotorCode.WHEELS_FORWARD if rightSpeed >= 0 else MotorCode.WHEELS_BACKWORD
    serial.write_motor_command(left_motor_code, right_motor_code, abs(leftSpeed), abs(rightSpeed))