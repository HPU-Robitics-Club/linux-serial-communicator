from approxeng.input.selectbinder import ControllerResource
from serial_communicator import SerialCommunicator, MotorCode
from time import sleep

def registerControllerListener(serial: SerialCommunicator):
    while True:
        # Checks to make sure joystick is connected
        try: 
            with ControllerResource() as joystick:
                print('Found joystick!')
                while joystick.connected:
                    x = joystick.rx
                    y = joystick.ry

                    #print(f'x = {x}')
                    #print(f'y = {y}')
                    
                    leftSpeed = 0
                    rightSpeed = 0
                    # Parses raw controller values
                    if abs(x) > 0.1 or abs(y) > 0.1:
                        # Acquires the sign of x and y
                        ySine = abs(y)/y if y != 0 else 1
                        xSine = abs(x)/x if x != 0 else 1

                        if abs(x) <= 0.25:
                            leftSpeed = y * 127 + ySine * 128
                            rightSpeed = leftSpeed
                        else:
                            # Makes the forward turning joystick events have a little more leeway before going to the backward turning
                            if ySine < 0 and y > -0.15:
                                ySine = +1

                            # Makes only one of the sides move for the turns, starting at 128
                            if x > 0:
                                leftSpeed = ySine * (x * 127 + xSine * 128)
                            else:
                                rightSpeed = -ySine * (x * 127 + xSine * 128)
                                
                    # Parses and then send the parsed motor code
                    parseAndSendMotorCode(leftSpeed, rightSpeed, serial)

        except IOError:
            print("Unable to find joystick!")
            sleep(1.0)

def parseAndSendMotorCode(leftSpeed: int, rightSpeed: int, serial):
    leftSpeed = round(leftSpeed) if abs(leftSpeed) > 30 else 0
    rightSpeed = round(rightSpeed) if abs(rightSpeed) > 30 else 0
    # print(f'leftSpeed = {leftSpeed}, rightSpeed = {rightSpeed}')
    left_motor_code = MotorCode.WHEELS_FORWARD if leftSpeed >= 0 else MotorCode.WHEELS_BACKWARD
    right_motor_code = MotorCode.WHEELS_FORWARD if rightSpeed >= 0 else MotorCode.WHEELS_BACKWARD
    serial.write_motor_command(left_motor_code, right_motor_code, abs(leftSpeed), abs(rightSpeed))

