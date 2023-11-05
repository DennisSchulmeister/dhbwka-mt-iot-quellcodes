#! /usr/bin/env python3

"""
Testprogramm zur Fehlersuche bei den Motor-Pins.
"""

from gpiozero import DigitalOutputDevice
import signal

pins = []

for pin in [23, 24, 27, 22]:
    pins.append(DigitalOutputDevice(pin))

print("Alle Pins an!")
for pin in pins:
    pin.on()

try:
    signal.pause()
except KeyboardInterrupt:
    pass

print("Alle Pins aus!")
for pin in pins:
    pin.off()