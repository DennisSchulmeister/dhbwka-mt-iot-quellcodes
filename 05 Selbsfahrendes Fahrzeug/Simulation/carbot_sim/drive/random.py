import random
from carbot_sim.utils import InfiniteTask

class RandomDrive(InfiniteTask):
    """
    Fahrstrategie: Willkürlich rumkurven.
    """
    def __init__(self, update_frequency, vehicle, min_count, max_count):
        """
        Konstruktor. Parameter:
            * update_frequency: UpdateFrequency-Objekt
            * vehicle: Objekt zur Fahrzeugsteuerung
            * min_count: Frühestes nach X Intervallen die Richtung ändern
            * max_count: Spätestend nach X Intervallen die Richtung ändern
        """
        super().__init__(update_frequency, vehicle)

        self._prev_direction = 0
        self._next_change = 0
        self._current_count = -0
        self._min_count = min_count
        self._max_count = max_count

    def _update(self):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        self._current_count += 1

        if self._current_count < self._next_change:
            return
        
        self._next_change = random.randint(self._min_count, self._max_count)
        self._current_count = 0

        self._vehicle.direction = (random.randint(0, 10) - 5) / 10.0

        if self._prev_direction < 0 and self._vehicle.direction < 0 \
        or self._prev_direction > 0 and self._vehicle.direction > 0:
            self._vehicle.direction *= -1

        self._prev_direction = self._vehicle.direction
        
        speed = random.randint(4, 10) / 10.0
        self._vehicle.target_speed = speed