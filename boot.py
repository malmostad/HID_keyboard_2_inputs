import usb_hid
import storage
import usb_cdc

# Inaktivera USB-minnet (CIRCUITPY) så att Linux inte blir förvirrat
storage.disable()
# Inaktivera seriell port
usb_cdc.disable()
# Aktivera endast tangentbordet
usb_hid.enable((usb_hid.Device.KEYBOARD,))
