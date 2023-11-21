#!/usr/bin/env python

import psutil, time

def main():
    """Hauptfunktion"""
    while True:
        # Die folgende Funktion liefert ein Tupel mit fünf Werten zurück
        memory_info = psutil.virtual_memory()

        print("\033c", end='')
        print(f"Hauptspeicher Gesamt...: {round(memory_info[0] / 1024 / 1024, 2)} MB")
        print(f"Verfügbarer Speicher...: {round(memory_info[1] / 1024 / 1024, 2)} MB")
        print(f"Speicherauslastung.....: {round(memory_info[1] / memory_info[0] * 100, 2)} %")
        print()
        print("Strg+C drücken zum Beenden!", flush=True)

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass