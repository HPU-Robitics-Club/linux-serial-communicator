from serial_communicator import SerialCommunicator, MotorCode
from controller_listener import registerControllerListener

serial = SerialCommunicator() 
registerControllerListener(serial)
