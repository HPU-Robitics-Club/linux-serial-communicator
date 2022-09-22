from serial_communicator import MotorCode, SerialCommunicator
import keyboard

def on_keyboard_press(key):
    print(key)

listener = keyboard.on_press(on_keyboard_press)

serial = SerialCommunicator()