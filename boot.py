# boot.py
import usb_hid
import storage
import usb_cdc

# Inaktivera USB-minnet (CIRCUITPY-drivenheten)
storage.disable()
# Inaktivera den seriella konsolen
usb_cdc.disable()
# Aktivera endast tangentbordet
usb_hid.enable((usb_hid.Device.KEYBOARD,))
