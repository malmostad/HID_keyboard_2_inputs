#  Makes a Raspberry Pi Pico act as a HID keyboard with the sole purpose of
#  sending a keycode when a switch between GP1 and GND is opened or closed.
#  Specifically intended to be used with Blocks together with triggering headphones from
#  https://www.interpretationshop.co.uk/product/heavy-duty-handset-standard-autoplay/
#  Logic of the sketch: When headphone is lifted (switch opened), keycode "1" is sent.
#  When headphone is hung back, keycode "0" is sent.
#  2022-10-12 David Cinthio, Malmö museer

import time
import board
import usb_hid
import digitalio
from adafruit_hid import keyboard
from digitalio import DigitalInOut, Direction, Pull

#  Pinout below for Pi Pico
btnswitch1 = digitalio.DigitalInOut(board.GP18)
btnswitch1.direction = digitalio.Direction.INPUT
btnswitch1.pull = digitalio.Pull.UP
prev_state1 = btnswitch1.value

btnswitch2 = digitalio.DigitalInOut(board.GP19)
btnswitch2.direction = digitalio.Direction.INPUT
btnswitch2.pull = digitalio.Pull.UP
prev_state2 = btnswitch2.value

kbd = keyboard.Keyboard(usb_hid.devices)

while True:
    cur_state1 = btnswitch1.value
    cur_state2 = btnswitch2.value
    if cur_state1 != prev_state1 or cur_state2 != prev_state2:
        if (not cur_state1) and (not cur_state2):
            # if both headphones are down, stop playing
            print("Send keycode 1, Stop")
            kbd.release(keyboard.Keycode.ONE)
            # start playing if one of the headphones are picked up (and none were picked up before)
        elif (cur_state1 and not prev_state2) or (cur_state2 and not prev_state1):
            print("Send keycode 1, Play")
            kbd.press(keyboard.Keycode.ONE)

    prev_state1 = cur_state1
    prev_state2 = cur_state2
