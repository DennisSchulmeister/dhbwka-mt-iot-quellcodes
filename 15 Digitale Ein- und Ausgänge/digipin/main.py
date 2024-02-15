"""
Beispiel zum Entprellen von Hardware-Buttons. Diese Beispiel verwendet zwei Buttons,
von denen einer die LED ein- und der andere sie wieder ausschaltet. Wird kein Butto
gedrückt, behält die LED ihren letzten Zustand.

Hardwareaufbau:
---------------

 - [GPIO 2] --> [Erster Button] --> [GND]
 - [GPIO 3] --> [Zweiter Button] --> [GND]
 - [GPIO 17] --> [LED] --> [Widerstand 300 Ohm] --> [GND]

Für die Button-Pins wird der eingebaute Pull-Up-Widerstand des Raspberry Pi
aktiviert. Die Buttons müssen das Signal daher beim Drücken auf Ground runterziehen.

Falls das X40 Sensor Kit verwendet wird, wird kein Widerstand für die LED benötigt, da
dieser bereits auf dem LED-Modul enthalten ist. Andernfalls kann ein beliebiger Widerstand
ab ca. 300 Ohm verwendet werden, um die Stromstärke für die LED zu begrenzen.

Relevante Dokumentation
-----------------------

https://gpiozero.readthedocs.io/en/stable/api_input.html#button
https://gpiozero.readthedocs.io/en/stable/api_output.html#led
"""

import signal
from gpiozero import Button, LED

def main():
    button1 = Button(2, pull_up=True, bounce_time=0.1)
    button2 = Button(3, pull_up=True, bounce_time=0.1)
    led     = LED(17)

    button1.when_pressed = led.on
    button2.when_pressed = led.off

    print("Drücken Sie Strg+C zum Beenden")

    try:
        signal.pause()
    except KeyboardInterrupt:
        pass
