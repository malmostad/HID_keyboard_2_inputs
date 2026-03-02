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
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# --- INITIALISERING ---
# Vänta 10 sekunder för att låta NUC:en boota färdigt
time.sleep(10)

# Setup för brytarna på GP18 och GP19
btnswitch1 = digitalio.DigitalInOut(board.GP18)
btnswitch1.direction = digitalio.Direction.INPUT
btnswitch1.pull = digitalio.Pull.UP

btnswitch2 = digitalio.DigitalInOut(board.GP19)
btnswitch2.direction = digitalio.Direction.INPUT
btnswitch2.pull = digitalio.Pull.UP

prev_state1 = btnswitch1.value
prev_state2 = btnswitch2.value

# --- HUVUDLOOP MED FELHANTERING ---
while True:
    try:
        # Skapa tangentbordsobjektet
        kbd = Keyboard(usb_hid.devices)
        
        while True:
            cur_state1 = btnswitch1.value
            cur_state2 = btnswitch2.value
            
            # Om något har ändrats på brytarna
            if cur_state1 != prev_state1 or cur_state2 != prev_state2:
                
                # Om båda lurarna läggs ner
                if (not cur_state1) and (not cur_state2):
                    kbd.release(Keycode.ONE)
                
                # Om en lur lyfts (och den andra inte redan var uppe)
                elif (cur_state1 and not prev_state2) or (cur_state2 and not prev_state1):
                    kbd.press(Keycode.ONE)

                prev_state1 = cur_state1
                prev_state2 = cur_state2
            
            # Debounce (50ms) för att undvika fladder
            time.sleep(0.05)

    except Exception as e:
        # Om USB-kommunikationen bryts, vänta 5 sek och försök igen
        time.sleep(5)
