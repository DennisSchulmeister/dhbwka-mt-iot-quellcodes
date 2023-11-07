from gpiozero import DistanceSensor
from carbot_sim.utils import InfiniteTask

class ObstacleSensor(InfiniteTask):
    """
    Ultraschall-Sensor zur Erkennung von Hindernissen in der Fahrlinie.
    """
    
    def __init__(self, update_frequency, vehicle, trigger, echo, min_cm, max_cm):
        """
        Konsturktor. Parameter:

            * update_frequency: UpdateFrequency-Objekt
            * vehicle: Objekt zur Fahrzeugsteuerung
            * trigger: Pinnummer für Trigger-Signal
            * echo: Pinnummer für Echo-Signal
            * min_cm: Einzuhalteneder Mindestabstand in cm
            * max_cm: Abstand in cm ab wann das Fahrzeug abgebremst wird
        """
        super().__init__(update_frequency, vehicle)

        self._sensor   = DistanceSensor(trigger=trigger, echo=echo)
        self._min_cm   = min_cm
        self._max_cm   = max_cm
        self._range_cm = self._max_cm - self._min_cm
    
    def _update(self):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        distance_cm = self._sensor.distance * 100

        if distance_cm < self._min_cm:
            self._vehicle.obstacle_pushback = 1
        elif distance_cm > self._max_cm:
            self._vehicle.obstacle_pushback = 0
        else:
            self._vehicle.obstacle_pushback = (distance_cm - self._min_cm) / self._range_cm