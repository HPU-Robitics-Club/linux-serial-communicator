from approxeng.input.selectbinder import ControllerResource

# Get a joystick
with ControllerResource() as joystick:
    # Loop until disconnected
    while joystick.connected:
        # Get a corrected value for the left stick x-axis
        left_x = joystick['lx']
        # We can also get values as attributes:
        left_y = joystick.ly