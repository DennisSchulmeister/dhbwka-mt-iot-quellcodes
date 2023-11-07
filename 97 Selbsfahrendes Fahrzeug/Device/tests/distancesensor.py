#! /usr/bin/env python3

"""
Testprogramm für einen einfachen Ultraschallabstandssensor mit gpiozero.
Praktischerweise hat gpiozero eine fertige Klasse eingebaut, welche die
technischen Details komplett verbirgt.

Vgl. https://osoyoo.com/2020/08/01/osoyoo-raspberry-pi-v2-0-car-lesson-3-obstacle-avoidance/
"""

from gpiozero import DistanceSensor
from time import sleep

try:
    # pigpio-Bibliothek für höhere Genauigkeit verwenden, falls installiert
    from gpiozero.pins.pigpio import PiGPIOFactory
    from gpiozero import Device
    Device.pin_factory = PiGPIOFactory()
    print("Benutze pigpio für höhere Genauigkeit")
except:
    pass

sensor = DistanceSensor(echo=21, trigger=20)

try:
    while True:
        distance_cm = sensor.distance * 100
        print(f"Abstand: {distance_cm} cm")
        sleep(1)
except KeyboardInterrupt:
    pass