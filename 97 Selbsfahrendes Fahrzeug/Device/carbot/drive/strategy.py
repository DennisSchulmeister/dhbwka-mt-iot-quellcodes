import random, time

from carbot.sensors.base import SensorBase

class BackAndForthDrive(SensorBase):
    """
    Fahrstrategie: Vor- und zurück ohne zu lenken.
    """
    def __init__(self, direction_change):
        """
        Konsturktor. Parameter:
            * direction_change: Funktion zum Prüfen auf Richtungswechsel
        """
        super().__init__()
        self._direction_change = direction_change

    def update(self, vehicle):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        try:
            change = self._direction_change.__next__()
        except:
            return
        
        if change:
            vehicle.direction = 0
            speed = random.randint(0, 10) / 10.0

            if vehicle.target_speed >= 0:
                vehicle.target_speed = speed * -1
            else:
                vehicle.target_speed = speed

class RandomDrive(SensorBase):
    """
    Fahrstrategie: Willkürlich rumkurven.
    """
    def __init__(self, direction_change):
        """
        Konstruktor. Parameter:
            * direction_change: Funktion zum Prüfen auf Richtungswechsel
        """
        super().__init__()
        self._direction_change = direction_change
        self._prev_direction = 0

    def update(self, vehicle):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        try:
            change = self._direction_change.__next__()
        except:
            return
        
        if change:
            vehicle.direction = (random.randint(0, 10) - 5) / 10.0

            if self._prev_direction < 0 and vehicle.direction < 0 \
            or self._prev_direction > 0 and vehicle.direction > 0:
            	vehicle.direction *= -1

            self._prev_direction = vehicle.direction
            
            speed = random.randint(4, 10) / 10.0
            vehicle.target_speed = speed

class FollowLineDrive(SensorBase):
    """
    Fahrstrategie: Bodenlinie folgen. Funktioniert nur, wenn der LineSensor
    aktiv ist und die Fahrlinie erkennt. Das Fahrzeug wird entsprechend der
    erkannten Bodenlinie vorwärts gelenkt. Bei nicht erkannter Linie fährt
    es für ein paar Sekunden langsam rückwärts, um die Linie zu suchen.
    """

    STATUS_DRIVING, STATUS_SEARCHING, STATUS_LOST = 0, 1, 2

    def __init__(self, forward_speed=1.0, backward_speed=-0.5, search_timeout_s=5):
        """
        Konstruktor. Parameter:

            * forward_speed: Normale Vorwärtsfahrgeschwindigkeit
            * backward_speed: Rückwärtsfahrgeschwindigkeit beim Suchen der Fahrlinie
            * search_timeout_s: Maximale Zeit zum Suchen der Fahrlinie in Sekunden
        """
        self._forward_speed     = forward_speed
        self._backward_speed    = backward_speed
        self._search_timeout_s  = search_timeout_s
        self._search_start_time = 0

        if self._forward_speed < 1:
            self._forward_speed *= -1
        
        if self._backward_speed > 1:
            self._backward_speed *= -1

        self.status = self.STATUS_DRIVING

    def update(self, vehicle):
        """
        Sensor prüfen und Fahrzeugparameter anpassen.
        """
        if self.status == self.STATUS_SEARCHING:
            # Fahrlinie suchen, aber nur innerhalb der gegebenen Zeit.
            # Sonst wechselt der Status auf STATUS_LOST, da die Fahrlinie nicht gefunden wurde.
            if time.monotonic() - self._search_start_time > self._search_timeout_s:
                self.status = self.STATUS_LOST
            else:
                vehicle.target_speed = self._backward_speed
                vehicle.direction = 0
        else:
            # Normale Vorwärtsfahrt, sofern eine Fahrlinie erkannt wurde.
            # Falls nein, Suche starten. Es sei denn, es wurde schon erfolglos gesucht.
            if vehicle.line_pattern == (0,0,0,0,0):
                if self.status != self.STATUS_LOST:
                    self.status = self.STATUS_SEARCHING
                return

            self.status = self.STATUS_DRIVING
            vehicle.target_speed = self._forward_speed

            # Vorwärts fahren
            if vehicle.line_pattern == (1,1,1,1,1) \
            or vehicle.line_pattern == (0,1,1,1,0) \
            or vehicle.line_pattern == (0,0,1,0,0):
                vehicle.direction = 0

            # Nach links korrigieren
            elif vehicle.line_pattern == (0,1,1,1,1):
                vehicle.direction = -0.2
            elif vehicle.line_pattern == (0,0,1,1,1):
                vehicle.direction = -0.4
            elif vehicle.line_pattern == (0,0,0,1,1):
                vehicle.direction = -0.6
            elif vehicle.line_pattern == (0,0,0,0,1):
                vehicle.direction = -0.8
            elif vehicle.line_pattern == (0,0,1,1,0) \
              or vehicle.line_pattern == (0,0,0,1,0):
                vehicle.direction = -0.5
            
            # Nach rechts korrigieren
            elif vehicle.line_pattern == (1,1,1,1,0):
                vehicle.direction = 0.2
            elif vehicle.line_pattern == (1,1,1,0,0):
                vehicle.direction = 0.4
            elif vehicle.line_pattern == (1,1,0,0,0):
                vehicle.direction = 0.6
            elif vehicle.line_pattern == (1,0,0,0,0):
                vehicle.direction = 0.8
            elif vehicle.line_pattern == (0,1,1,0,0) \
              or vehicle.line_pattern == (0,1,0,0,0):
                vehicle.direction = 0.5
