import time
import board
import usb_hid
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# --- INITIALISERING ---
# Vänta 10 sekunder så att NUC:en hinner boota helt
time.sleep(10)

# Setup för en hörlur på GP18
handset = digitalio.DigitalInOut(board.GP18)
handset.direction = digitalio.Direction.INPUT
handset.pull = digitalio.Pull.UP

# Håll koll på tidigare läge
prev_lifted = handset.value

print("Systemet redo för en hörlur (GP18)...")

# --- HUVUDLOOP ---
while True:
    try:
        # Initiera tangentbordet
        kbd = Keyboard(usb_hid.devices)
        
        while True:
            # Läs av om luren är lyft (True) eller på plats (False)
            is_lifted = handset.value
            
            if is_lifted != prev_lifted:
                if is_lifted:
                    # Hörlur lyfts -> Skicka 1 (Play)
                    print("Hörlur lyft - Play")
                    kbd.press(Keycode.ONE)
                else:
                    # Hörlur läggs tillbaka -> Släpp 1 (Stop)
                    print("Hörlur nere - Stop")
                    kbd.release(Keycode.ONE)

                prev_lifted = is_lifted
            
            # Kort paus för stabilitet
            time.sleep(0.05)

    except Exception as e:
        # Om USB-anslutningen svajar, vänta 5 sekunder och försök igen
        time.sleep(5)
