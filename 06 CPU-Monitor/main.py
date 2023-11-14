#!/usr/bin/env python

import psutil, time

def read_sensor_value():
    """
    Sensorwert auslesen. Liefert der Einfachheit halber die aktuelle CPU-Auslastung
    der letzten Sekunde in Prozent zurück.
    """
    return psutil.cpu_percent(1)

def main():
    """Hauptfunktion"""
    measurements = []
    MAX_NUM_MEASUREMENTS = 10

    while True:
        # Die folgenden Zeilen berechnen einen gleitenden Durchschnitt der letzten
        # MAX_NUM_MEASUREMENTS Messwerte
        measurements.append(read_sensor_value())
        measurements = measurements[-MAX_NUM_MEASUREMENTS:]

        average = sum(measurements) / len(measurements)

        print("\033c", end='')
        print(f"CPU-Auslastung (aktuell): {round(measurements[-1], 2)} %")
        print(f"CPU-Auslastung (schnitt): {round(average, 2)} %")
        print()
        print("Strg+C drücken zum Beenden!", flush=True)

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass