from gpiozero import DistanceSensor
from carbot.sensors.base import SensorBase

class ObstacleSensor(SensorBase):
    """
    Ultraschall-Sensor zur Erkennung von Hindernissen in der Fahrlinie.
    """
    
    def __init__(self, trigger, echo, min_cm, max_cm):
        """
        Konsturktor. Parameter:

            * trigger: Pinnummer für Trigger-Signal
            * echo: Pinnummer für Echo-Signal
            * min_cm: Einzuhalteneder Mindestabstand in cm
            * max_cm: Abstand in cm ab wann das Fahrzeug abgebremst wird
        """
        super().__init__()

        self._sensor   = DistanceSensor(trigger=trigger, echo=echo)
        self._min_cm   = min_cm
        self._max_cm   = max_cm
        self._range_cm = self._max_cm - self._min_cm
    
    def update(self, vehicle):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        distance_cm = self._sensor.distance * 100

        if distance_cm < self._min_cm:
            vehicle.obstacle_pushback = 1
        elif distance_cm > self._max_cm:
            vehicle.obstacle_pushback = 0
        else:
            vehicle.obstacle_pushback = (distance_cm - self._min_cm) / self._range_cm