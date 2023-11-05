#! /usr/bin/env python3
"""
Startskript für das carbot_sim-Program. Startet eine tkgpio-Simulation des
Fahrzeugcodes.
"""

import asyncio, json, os

from tkgpio import TkCircuit
from carbot_sim.main import main

if __name__ == "__main__":
    try:
	# HINWEIS: Unter Windows die Datei tkgpio_windows.json eintragen
        file_path = os.path.dirname(__file__)
        file_path = os.path.join(file_path, "tkgpio_linux.json")

        with open(file_path) as json_file:
            config = json.load(json_file)
        
        circuit = TkCircuit(config)
        circuit.run(lambda: asyncio.run(main()))
    except KeyboardInterrupt:
        pass
