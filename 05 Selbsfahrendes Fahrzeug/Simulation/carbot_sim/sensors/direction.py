from carbot_sim.utils import InfiniteTask
from gpiozero import Servo

class DirectionServo(InfiniteTask):
    """
    Servomotor, mit dem der Ultraschall-Sensor in Fahrtrichtung gedreht werden kann.
    """

    def __init__(self, pin, update_frequency, vehicle):
        """
        Konsturktor. Parameter:

            * pin: GPIO-Pin des Servomotors
            * update_frequency: UpdateFrequency-Objekt
            * vehicle: Objekt zur Fahrzeugsteuerung
        """
        super().__init__(update_frequency, vehicle)
        self._servo = Servo(pin)

    def _update(self):
        """
        Servo anhand der Fahrtichtung drehen. Die Fahrtrichtung wird als
        Zahl [-1...1] gesteuert und hier in einen Winkel von [10°-170°]
        umgerechnet.
        """
        self._servo.value = self._vehicle.direction * 0.9