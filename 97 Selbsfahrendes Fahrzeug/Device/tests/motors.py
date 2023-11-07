#! /usr/bin/env python3

"""
Testprogramm für die Antriebsmotoren des "OSOYOO Raspberry Pi V2.0 Car" Fahrzeugs.
Das Fahrzeug besitzt je einen Motor für das linke und das rechte Rad, die hier
zunächst einzeln und dann gemeinsam angesteuert werden. Das Fahrzeug sollte hierfür
auf einer größeren, freien Fläche stehen oder auf dem Rücken liegen. :-)

Hier kommen wie beim Servo-Testprogramm wieder die Spezialbibliotheken von Adafruit
Circuitpython zur PWM-Steuerung mit PCA9685-Baustein zum Einsatz. Dieser wird in
dem Fahrzeug verwendet, um ein besseres Timing als mit der nativen Pulsweitenmodulation
des Raspberry Pi zu erhalten.

Vgl. https://osoyoo.com/2020/08/01/how-to-use-osoyoo-model-pi-l298n-motor-driver-board-in-raspberry-pi-robot-car/
"""

import time, signal

# https://docs.circuitpython.org/en/latest/shared-bindings/board/index.html
# https://docs.circuitpython.org/en/latest/shared-bindings/busio/index.html
# https://docs.circuitpython.org/projects/pca9685/en/latest/index.html
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from gpiozero import DigitalOutputDevice

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 60

class PCA9685Motor:
    """
    Hilfsklasse zur Steuerung eines Motors in Anlehnung an `gpiozero.Motor`.
    Da die Pulsweitenmodulation hier nicht vom Raspberry Pi sondern über einen
    externen PCA9685-Baustein gesteuert wird, ist es am einfachstn, eine eigene
    Klasse zur Ansteuerung eines Motors zu schreiben und sich bei der Schnittstelle
    an `gpiozero.Motor` zu orientieren.

    Auf Hardwarebene funktioniert die Ansteuerung wie folgt:

     * Jeder Motor ist mit zwei GPIO-Ausgängen verbunden, welche die Drehrichtung
       steuern. Der eine Pin signalisiert dem Motor Vorwärtsfahrt, der andere Pin
       Rückwärtsfahrt. Dementsprechend muss immer genau einer der beiden Pins aktiv
       sein, damit der Motor fahren kann. Beide Pins aktiv oder beide Pins inaktiv
       bedeutet Stopp.
    
     * Zusätzlich erhält jeder Motor über den PCA9685-Baustein ein PWM-Signal zur
       Steuerung der Geschwindigkeit.
    
    Geschwindigkeit und Richtung des Motors können mit dieser Klasse wie folgt
    geändert werden:

     * Methode `forward(0.0 ... 1.0)`: Vorwärtsfahrt
     * Methode `backward(0.0 ... 1.0)`: Rückwärtsfahrt
     * Methode `reverse()`: Fahrtrichtung umkehren
     * Methode `stop()`: Anhalten
     * Zuweisung an Attribut `value` = -1.0 ... 1.0
    """
    def __init__(self, forward, backward, pwmChannel):
        self._forward    = DigitalOutputDevice(forward)
        self._backward   = DigitalOutputDevice(backward)
        self._pwmChannel = pca.channels[pwmChannel]
        self._value      = 0
    
    def forward(self, speed):
        self.value = speed
    
    def backward(self, speed):
        self.value = speed * -1
    
    def stop(self):
        self.value = 0
    
    def is_active(self):
        return self.value != 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self._pwmChannel.duty_cycle = int(0xFFFF * abs(value))

        if value > 0:
            self._forward.on()
            self._backward.off()
        elif value < 0:
            self._forward.off()
            self._backward.on()
        else:
            self._forward.off()
            self._backward.off()

motor1 = PCA9685Motor(24, 23, 0)
motor2 = PCA9685Motor(22, 27, 1)

try:
    for motor in [motor1, motor2]:
        print(motor)

        for speed in range(-10, 10):
            motor.value = speed / 10
            print(f" - {motor.value}")
            time.sleep(0.5)
        
        motor1.value = 0
        motor2.value = 0
        
        print()
except KeyboardInterrupt:
    pass

try:
    print("Both motors")
    for speed in range(-10, 10):
        motor1.value = speed / 10
        motor2.value = speed / 20
        print(f" - {motor1.value}, {motor2.value}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

# try:
#     print("Full power forwards")
#     motor1.value = 1
#     motor2.value = 1

#     # time.sleep(5)
#     signal.pause()
# except KeyboardInterrupt:
#     pass

motor1.value = 0
motor2.value = 0