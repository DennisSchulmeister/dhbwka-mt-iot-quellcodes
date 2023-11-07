from carbot_sim.utils import InfiniteTask

class LineSensor(InfiniteTask):
    """
    Infrarot-Linesensor zur Erkennung von Farbahnmarkierungen auf dem Boden.
    Der Sensor leuchtet hierfür fünf nebeneinander liegenden Punkte mit
    Infrarotlicht aus und misst die Reflektion.
    """
    def __init__(self, update_frequency, vehicle):
        """
        Konsturktor. Parameter:

            * update_frequency: UpdateFrequency-Objekt
            * vehicle: Objekt zur Fahrzeugsteuerung
        """
        super().__init__(update_frequency, vehicle)
    
    def _update(self):
        """
        AUFGABE: Linesensor abfragen und Fahrzeugparameter entsprechend anpassen
        """
        pass
