#! /usr/bin/env python
"""
Einparkhilfe
============

Fallbeispiel für eine einfache Einparkhilfe, wie sie in Autos verbaut wird. Wird ein elektrischer
Kontakt geschlossen, während der Rückwärtsgang eingelegt ist, findet über einen Ultraschallsensor
eine regelmäßige Abstandsmessung statt. Die gemessene Entfernung wird durch einen periodischen
Signalton hörbar gemacht. Je kleiner der Abstand, desto schneller die Signaltöne bis hin zu einem
Dauerton bei Unterschreiten der Mindestdistanz.

Aufgrund von Reflexionen (Echos) des Ultraschallsignals schwankt die gemessene Distanz immer wieder
ein wenig. gpiozero glättet den Messwert daher und gibt immer einen Durschnitt aus mehreren, nacheinander
durchgeführten Messungen zurück.

Hardwareaufbau:
---------------

Hardware-Button:

         [GPIO 26] --> [Button Pin 1]
    [Button Pin 2] --> [GND]

Ultraschallsensor:

               [GPIO 27] --> [Level-Shifter A1]
      [Level Shifter B1] --> [Sensor Trigger]
           [Sensor Echo] --> [Level Shifter B2]
      [Level Shifter A2] --> [GPIO 22]
     [Level Shifter GND] --> [GND]
    [Level Shifter VCCa] --> [3.3V]
    [Level Shifter VCCb] --> [5V]
            [Sensor VCC] --> [5V]
            [Sensor GND] --> [GND]

  Da der Sensor mit 5V Logikpegel arbeitet, der Pi aber nur mit 3.3V, benötigen wir einen Level-Shifter,
  der die beiden Spannungen ineinander konvertiert.

Aktiver Buzzer / Signalgeber:

        [GPIO 21] --> [Buzzer SIGNAL]
     [Buzzer GND] --> [Arduino GND]

  Falls statt einem aktiven Piezo-Buzzer eine LED angeschlossen wird, sollte ein Widerstand
  in Reihe eingebaut werden, um die Stromstärke zu besgrenzen.

Relevante Dokumentation
-----------------------

https://sensorkit.joy-it.net/de/sensors/ky-050
https://sensorkit.joy-it.net/de/sensors/ky-006
https://gpiozero.readthedocs.io/en/stable/api_input.html#button
https://gpiozero.readthedocs.io/en/stable/api_output.html#led
https://gpiozero.readthedocs.io/en/stable/recipes.html#distance-sensor
"""

import time
from gpiozero import Button, DistanceSensor, Buzzer

DISTANCE_MIN_CM    = 3.0
DISTANCE_MAX_CM    = 30.0
DISTANCE_INFINITY  = 99999
FREQUENCY_MIN_HZ   = 1.0
FREQUENCY_MAX_HZ   = 8.00

def main():
    button = Button(26, pull_up=True, bounce_time=0.1)
    sensor = DistanceSensor(trigger=27, echo=22)
    buzzer = Buzzer(21)

    print("Drücken Sie Strg+C zum Beenden")

    try:
        while True:
            time.sleep(0.001)

            if button.is_pressed:
                print("Starte Messung")
                distance_cm = sensor.distance * 100
                print(f"Gemessene Distanz: {distance_cm} cm")
            else:
                distance_cm = DISTANCE_INFINITY

            if distance_cm < DISTANCE_MIN_CM:
                buzzer.on()
            elif distance_cm > DISTANCE_MAX_CM:
                buzzer.off()
            else:
                percent      = (distance_cm - DISTANCE_MIN_CM) / (DISTANCE_MAX_CM - DISTANCE_MIN_CM)
                frequency_hz = ((1 - percent) * (FREQUENCY_MAX_HZ - FREQUENCY_MIN_HZ)) + FREQUENCY_MIN_HZ
                half_cycle_s = (1 / frequency_hz) / 2

                buzzer.beep(on_time=half_cycle_s, off_time=half_cycle_s)
    except KeyboardInterrupt:
        pass
