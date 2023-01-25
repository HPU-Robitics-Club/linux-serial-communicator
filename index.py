from serial_communicator import SerialCommunicator
from controller_listener import registerControllerListener

serial = SerialCommunicator()
registerControllerListener(serial)
