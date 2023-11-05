#! /usr/bin/env python3

"""
Testprogramm für den Trackingsensor des "OSOYOO Raspberry Pi V2.0 Car" Fahrzeugs.
Der Sensor besteht aus fünf nebeneinander angeordneten und auf den Boden ausgerichteten
Infrarot-Sensoren, mit denen jeweils ein heller und ein dunkler Untergrund erkannt werden
kann. Dies kann genutzt werden, um einer dicken schwarzen Linie auf hellem Grund (oder
umgekehrt) zu folgen und dabei zu erkennen, ob die Line eine Kurve macht.

Die Sensoren besitzen hierfür eine Infrarot-LED und einen Phototransistor, dessen
Widerstand sich in Abhängigkeit vom reflektierten Licht ändert. Er kann daher aus Sicht
des Rasbperry Pi wie ein einfacher Schalter betrachtet werden, der bei dunklem Untergrund
einen Kontakt schließt. Folgerichtig wird hierfür die `Button`-Klasse von gpiozero in
diesem Testprogramm verwendet. 


Vgl. https://osoyoo.com/2020/08/01/osoyoo-raspberry-pi-v2-0-car-lesson-2-line-tracking/
"""

from gpiozero import Button
import time

PINS = [5, 6, 13, 19, 26]
values = []

def _callback(device):
    try:
        index = PINS.index(device.pin.number)
        values[index] = device.value
    except ValueError:
        pass

i = -1
for pin in PINS:
    i += 1
    values.append(0)

    sensor = Button(pin)

    sensor.when_pressed = _callback
    sensor.when_released = _callback

try:
    print("Strg+C zum Beenden drücken ...")
    print(values)

    while True:
        prev_values = values.copy()
        time.sleep(0.25)

        if values != prev_values:
            print(values)

except KeyboardInterrupt:
    pass
