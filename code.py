#  Makes a Raspberry Pi Pico act as a HID keyboard with the sole purpose of
#  sending a keycode when a switch between GP1 and GND is opened or closed.
#  Specifically intended to be used with Blocks together with triggering headphones from
#  https://www.interpretationshop.co.uk/product/heavy-duty-handset-standard-autoplay/
#  Logic of the sketch: When headphone is lifted (switch opened), keycode "1" is sent.
#  When headphone is hung back, keycode "0" is sent.
#  2022-10-12 David Cinthio, Malmö museer
#  This version 2026-03-02, David Cinthio, Malmö museum

import time
import board
import usb_hid
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# --- 1. STARTFÖRDRÖJNING ---
# Vänta 10 sekunder för att låta Linux/Blocks ladda drivrutiner
time.sleep(10)

# --- 2. LÄS DIN keys.conf ---
def get_config():
    try:
        with open("keys.conf", "r") as f:
            lines = f.readlines()
            # Rad 1: Pinnar (t.ex. board.GP18,board.GP19)
            pins_str = lines[0].strip().split(',')
            # Rad 2: Keycodes (t.ex. Keycode.KEYPAD_ONE,Keycode.KEYPAD_ZERO)
            keys_str = lines[1].strip().split(',')
            
            # Mappa strängar till faktiska objekt
            pins = [getattr(board, p.split('.')[-1]) for p in pins_str]
            codes = [getattr(Keycode, k.split('.')[-1]) for k in keys_str]
            return pins, codes
    except Exception as e:
        print(f"Kunde inte läsa keys.conf: {e}")
        # Standardvärden om filen saknas
        return [board.GP18, board.GP19], [Keycode.KEYPAD_ONE, Keycode.KEYPAD_ZERO]

target_pins, target_keys = get_config()

# --- 3. SETUP AV PINNAR ---
btn1 = digitalio.DigitalInOut(target_pins[0])
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

btn2 = digitalio.DigitalInOut(target_pins[1])
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP

prev_state1 = btn1.value
prev_state2 = btn2.value

# --- 4. HUVUDLOOP MED FELHANTERING ---
while True:
    try:
        kbd = Keyboard(usb_hid.devices)
        
        while True:
            cur_state1 = btn1.value
            cur_state2 = btn2.value
            
            if cur_state1 != prev_state1 or cur_state2 != prev_state2:
                # Logik för PLAY: Om en lur lyfts (True)
                if (cur_state1 and not prev_state2) or (cur_state2 and not prev_state1):
                    # Tryck på KEYPAD_ONE (från din conf)
                    kbd.press(target_keys[0])
                    time.sleep(0.1)
                    kbd.release(target_keys[0])
                
                # Logik för STOP: Om båda lurarna är nere (False)
                elif (not cur_state1) and (not cur_state2):
                    # Tryck på KEYPAD_ZERO (från din conf)
                    kbd.press(target_keys[1])
                    time.sleep(0.1)
                    kbd.release(target_keys[1])

                prev_state1 = cur_state1
                prev_state2 = cur_state2
            
            time.sleep(0.05) # Debounce

    except Exception as e:
        # Om USB-anslutningen svajar, vänta 5 sek och försök igen
        time.sleep(5)
