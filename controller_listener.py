from approxeng.input.selectbinder import ControllerResource
from serial_communicator import SerialCommunicator, MotorCode

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

                        if abs(x) <= 0.5:
                            leftSpeed = y * 127 + ySine * 128
                            rightSpeed = leftSpeed
                        else:
                            leftSpeed = x * 127 + xSine * 128
                            rightSpeed = -leftSpeed
                    
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

