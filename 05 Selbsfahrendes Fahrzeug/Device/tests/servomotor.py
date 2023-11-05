#! /usr/bin/env python3

"""
Testprogramm zum Ansteuern des Servomotors, mit dem der Distanzsensor und
die Kamera ausgerichtet werden. Ähnlich wie die Antriebsmotoren wird der
Servo über Pulsweitenmodulation. Das "OSOYOO Raspberry Pi V2.0 Car" nutzt
hierfür einen PCA9685-Baustein anstelle der PWM-Funktionen des RaspberyPi.

Die Ansteuerung erfolgt daher mit Bibliotheken von "Adafruit CircuitPython",
die einen Treiber für den PCA9685 besitzen. Leider ist die Dokumentation
dieses Bibliotheken etwas zerstreut und schwer zu finden, weshalb sie hier
bei den jeweiligen Imports verlinkt wurde.
"""

import time

# Boardspezifische PIN-Nummern
# https://docs.circuitpython.org/en/latest/shared-bindings/board/index.html
from board import SCL, SDA

# I2C/SPI-Kommunikation
# https://docs.circuitpython.org/en/latest/shared-bindings/busio/index.html
import busio

# Bibliothek zur PWM-Motorsteuerung
# https://docs.circuitpython.org/projects/motor/en/latest/
from adafruit_motor import servo

# Treiber für PCA6985-Board
# https://docs.circuitpython.org/projects/pca9685/en/latest/index.html
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 60

servomotor = servo.Servo(pca.channels[15], min_pulse=450, max_pulse=2150)

for r in [0, 85, 180, 85, 10, 170, 85, 20, 160, 45, 85, 135, 85]:
    print(r)
    servomotor.angle = r
    time.sleep(1)

pca.deinit()