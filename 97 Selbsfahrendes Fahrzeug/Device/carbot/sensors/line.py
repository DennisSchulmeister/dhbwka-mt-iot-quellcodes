from gpiozero import LineSensor as LineSensor_
from carbot.sensors.base import SensorBase

class LineSensor(SensorBase):
    """
    Infrarot-Linesensor zur Erkennung von Farbahnmarkierungen auf dem Boden.
    Der Sensor leuchtet hierfür fünf nebeneinander liegenden Punkte mit
    Infrarotlicht aus und misst die Reflektion.
    """

    BLACK, WHITE = 0, 1

    def __init__(self, pins, line_color=BLACK):
        """
        Konstruktor. Parameter:

            * pins: Liste mit den Pin-Nummern der Sensoren
            * line_color: Farbe der Fahrlinie
                * BLACK = Schwarze Linie auf weißem Grund
                * WHITE = Weiße Linie auf schwarzem Grund
        """
        self._line_color = line_color
        self._sensors = []

        for pin in pins:
            self._sensors.append(LineSensor_(pin))

    def update(self, vehicle):
        """
        Sensoren prüfen und die erkannte Markierung im Fahrzeugobjekt zur
        Auswertung beim autonomen Fahren ablegen.
        """
        line_pattern = []

        if self._line_color == self.BLACK:
            for sensor in self._sensors:
                line_pattern.append(1 if sensor.value < 0.5 else 0)
        else:
            for sensor in self._sensors:
                line_pattern.append(1 if sensor.value > 0.5 else 0)
        
        vehicle.line_pattern = tuple(line_pattern)
