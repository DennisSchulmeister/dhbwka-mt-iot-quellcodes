"""
Dies ist eine Variante des Beispiels zur Ansteuerung digitaler Bausteine.
Wir verwenden hier denselben Hardwareaufbau, jedoch wird die LED durch die
zwei Buttons nicht ein- oder ausgeschaltet, sondern mit PWM in ihrer Helligkeit
reguliert. Die beiden Buttons machen die LED je 10% heller oder dunkler.

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
https://gpiozero.readthedocs.io/en/stable/api_output.html#pwmled
"""

import time
from gpiozero import Button, PWMLED

def main():
    button1 = Button(2, pull_up=True, bounce_time=0.1)
    button2 = Button(3, pull_up=True, bounce_time=0.1)
    led     = PWMLED(17, initial_value=0.5)

    print("Drücken Sie Strg+C zum Beenden")

    try:
        while True:
            time.sleep(0.5)

            if button1.pressed:
                led.value -= 0.1
                led.value = max(0, led.value)
            elif button2.pressed:
                led.value += 0.1
                led.value = min(1, led.value)

    except KeyboardInterrupt:
        pass
