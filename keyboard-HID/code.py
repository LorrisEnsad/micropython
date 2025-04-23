# https://github.com/adafruit/Adafruit_CircuitPython_HID

import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

button_pins = [board.GP0, board.GP1, board.GP2, board.GP3]
key_mapping = [Keycode.UP_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW]

buttons = []
for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append(button)

last_states = [True] * 4

while True:
    for i in range(4):
        if not buttons[i].value and last_states[i]:
            kbd.press(key_mapping[i])
            last_states[i] = False
        elif buttons[i].value and not last_states[i]:
            kbd.release(key_mapping[i])
            last_states[i] = True
    time.sleep(0.01)


