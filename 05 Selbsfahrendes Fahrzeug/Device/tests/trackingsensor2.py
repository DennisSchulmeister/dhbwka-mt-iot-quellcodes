#! /usr/bin/env python3

"""
Testprogramm für den Trackingsensor des "OSOYOO Raspberry Pi V2.0 Car" Fahrzeugs.
Verwendet die Klasse `LineSensor` statt `Button` zum Test. Diese Klasse nutzt
ein Mehrfachsampling mit Glättung (Low Pass Filter), um Fehlerkennungen zu
minimieren. Die ausgegebenen Werte sind gegenüber `Button` invertiert:
0 = dunkel, 1 = hell

Vgl. https://osoyoo.com/2020/08/01/osoyoo-raspberry-pi-v2-0-car-lesson-2-line-tracking/
"""

from gpiozero import LineSensor
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

    sensor = LineSensor(pin)

    sensor.when_line = _callback
    sensor.when_no_line = _callback

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
