import random
from carbot_sim.utils import InfiniteTask

class ManualDrive(InfiniteTask):
    """
    Fahrstrategie: Handsteuerung über die vorgesehenen Taster.
    """
    def __init__(self, update_frequency, vehicle):
        """
        Konstruktor. Parameter:
            * update_frequency: UpdateFrequency-Objekt
            * vehicle: Objekt zur Fahrzeugsteuerung
        """
        super().__init__(update_frequency, vehicle)

    def _update(self):
        """
        AUFGABE:
         * Schalter an Pin 26 soll den Task "RandomDrive" pausieren
         * Buttons an den Pins 7 bis 12 sollen Geschwindigkeit und Fahrtrichtung ändern
        """
        pass