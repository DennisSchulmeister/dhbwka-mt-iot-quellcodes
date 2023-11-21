#!/usr/bin/env python

import os, random, time
from datetime import datetime

def main():
    """Hauptfunktion"""
    # Datei schreiben
    N = 5
    print(f"Starte {N} Messungen.")

    if os.path.exists("measurements.txt"):
        print("Datei existiert bereits.")
        mode = "a"
    else:
        print("Datei existiert noch nicht.")
        mode = "w"

    with open("measurements.txt", mode) as file:
        if mode == "w":
            file.write("timestamp\tvalue\n")

        for i in range(N):
            # Simulation einer Messung
            measurement = dict(timestamp=datetime.now(), value=random.randint(1, 1000))
            print(measurement)

            # Datenpunkt in Datei schreiben
            file.write(f"{measurement['timestamp']}\t{measurement['value']}\n")

            # Warten bis zur nächsten Messung
            time.sleep(random.randint(1, 3))
    
    # Dateiinhalt ausgeben
    print()
    print("Inhalt der Datei:")

    with open("measurements.txt", "r") as file:
        print(file.read())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass