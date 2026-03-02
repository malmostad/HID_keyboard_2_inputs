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

# --- INITIALISERING ---
# Vänta 10 sekunder så att NUC:en hinner boota och ladda USB-drivrutiner
time.sleep(10)

# Konfigurera GP18 och GP19 (Hörlur 1 och 2)
btn1 = digitalio.DigitalInOut(board.GP18)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

btn2 = digitalio.DigitalInOut(board.GP19)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP

# Håll koll på tidigare läge för att bara trigga vid förändring
prev_state1 = btn1.value
prev_state2 = btn2.value

# --- HUVUDLOOP ---
while True:
    try:
        # Skapa tangentbordsobjektet (initierar USB HID)
        kbd = Keyboard(usb_hid.devices)
        
        while True:
            cur_state1 = btn1.value
            cur_state2 = btn2.value
            
            # Har något ändrats?
            if cur_state1 != prev_state1 or cur_state2 != prev_state2:
                
                # Om BÅDA hörlurarna är nere (GND-slutna = False)
                if (not cur_state1) and (not cur_state2):
                    print("Båda nere - Stop")
                    kbd.release(Keycode.ONE)
                
                # Om minst en hörlur lyfts (Brytaren öppnas = True)
                elif (cur_state1 and not prev_state1) or (cur_state2 and not prev_state2):
                    print("Hörlur lyft - Play")
                    kbd.press(Keycode.ONE)

                # Uppdatera tillstånd för nästa varv
                prev_state1 = cur_state1
                prev_state2 = cur_state2
            
            # Debounce: En kort paus för att undvika "elektriskt fladder"
            time.sleep(0.05)

    except Exception as e:
        # Om USB-anslutningen inte är redo eller tappas, vänta 5 sek och försök igen
        # Detta hindrar programmet från att krascha helt.
        time.sleep(5)
        # Om USB-anslutningen svajar, vänta 5 sek och försök igen
        time.sleep(5)
