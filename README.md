Raspberry Pi Pico HID Handset Trigger
Gör en Raspberry Pi Pico till ett USB-tangentbord (HID) för att styra mediauppspelning i Pixilab Blocks. Systemet är designat för att känna av när en eller två hörlurar (handset) lyfts från sina fållor via magnetiska brytare.

Funktion
Lyft hörlur: Skickar tangenttryckning 1 (Keycode.ONE) för att starta media.

Häng tillbaka båda hörlurarna: Släpper tangenttryckning 1 för att stoppa media.

Anslutning: Enheten ansluts via USB till en Intel NUC (eller liknande Linux-baserad spelare).

Tekniska förbättringar (v2.0)
För att säkerställa att enheten fungerar tillförlitligt i en utställningsmiljö har följande ändringar gjorts jämfört med originalet:

Boot-stabilitet: En boot.py har lagts till för att dölja Picons USB-minne (CIRCUITPY) och seriella port vid start. Detta förhindrar att Linux-spelaren blir "förvirrad" under uppstartsprocessen.

Startfördröjning: Programmet väntar 10 sekunder vid strömsättning innan det försöker kommunicera via USB, vilket ger värddatorn tid att initiera sina drivrutiner.

Felhantering (Try-Except): Huvudloopen är inkapslad i felhantering. Om USB-förbindelsen tillfälligt tappas eller inte är redo, kraschar inte skriptet utan försöker återansluta automatiskt var 5:e sekund.

Hårdvarukonfiguration:

GP18: Hörlur 1 (Input Pull-up)

GP19: Hörlur 2 (Input Pull-up)

GND: Gemensam jord för brytarna

Installation
1. Filer
Ladda upp följande filer till din Pico:

boot.py: Konfigurerar USB-läget.

code.py: Innehåller huvudlogiken och felhanteringen.

2. Underhåll (Bootloader-läge)
Eftersom boot.py döljer USB-disken för att öka stabiliteten, kan du inte se filerna på Picon vid vanlig anslutning. För att gå in i programmeringsläge (så att disken dyker upp):

Via kod (i REPL/Thonny):

Python
import microcontroller
microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
microcontroller.reset()
Via hårdvara:
Om din Pico saknar BOOTSEL-knapp, kortslut TP1 (Test Point 1) mot GND samtidigt som du kopplar in USB-kabeln.

Testat med CircuitPython 10.1.3
https://circuitpython.org/board/raspberry_pi_pico/

Adafruit's Bundle Library:
adafruit-circuitpython-bundle-10.x-mpy-20260226
Använder adafruit_hid

Licens och Historik
Ursprunglig logik av David Cinthio (Malmö museum). Vidareutvecklad för ökad robusthet i Linux-miljöer 2026.
