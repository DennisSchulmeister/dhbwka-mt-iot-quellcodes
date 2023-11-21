#!/usr/bin/env python

import psutil, time

def read_sensor_values():
    """
    Auslesen der Sensorwerte. Liefert ein tief geschachteltes Dictionary mit
    folgenden Einträgen zurück:

        * memory:
            * total: Speicher gesamt (in Bytes)
            * available: Speicher verfügbar (in Bytes)
            * percent: Speicherauslastung (in Prozent)
        * cpu:
            * usage: CPU-Auslastung (in Prozent)
    """
    memory_info = psutil.virtual_memory()

    return {
        "memory": {
            "total":     memory_info[0],
            "available": memory_info[1],
            "percent":   memory_info[1] / memory_info[0],
        },
        "cpu": {
            "usage": psutil.cpu_percent(),
        },
    }

def display_sensor_values(sensor_values):
    """Anzeige der mit `read_sensor_values()` ermittelten Sensorwerte."""
    memory_total     = sensor_values["memory"]["total"] / 1024 / 1024
    memory_available = sensor_values["memory"]["available"] / 1024 / 1024
    memory_percent   = sensor_values["memory"]["percent"]
    cpu_usage        = sensor_values["cpu"]["usage"]

    print("\033c", end='')
    print("┌───────────────────────────────────────────────────────┐")
    print("│ Der IOT-Systemmonitor                                 │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ Hauptspeicher Gesamt...: %s MB                 │" % format(memory_total, "9.2f"))
    print("│ Verfügbarer Speicher...: %s MB                 │" % format(memory_available, "9.2f"))
    print("│ Speicherauslastung.....: %s %%                  │" % format(memory_percent, "9.2f"))
    print("├───────────────────────────────────────────────────────┤")
    print("│ CPU-Auslastung.........: %s %%                  │" % format(cpu_usage, "9.2f"))
    print("└───────────────────────────────────────────────────────┘")
    print()
    print(f"Strg+C drücken zum Beenden!", flush=True)

def main():
    """Hauptfunktion"""
    while True:
        sensor_values = read_sensor_values()
        display_sensor_values(sensor_values)

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass