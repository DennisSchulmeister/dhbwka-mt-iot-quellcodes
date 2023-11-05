from adafruit_motor import servo
from carbot.sensors.base import SensorBase

class DirectionServo(SensorBase):
    """
    Servomotor, mit dem die Kamera und der Ultraschall-Sensor in
    Fahrtrichtung gedreht werden kann.
    """

    def __init__(self, pca, pwmChannel, min_pulse=450, max_pulse=2150):
        """
        Konsturktor. Parameter:

            * pca: PCA9685-Objekt für die PWM-Steuerung
            * pwmChannel: PWM-Kanal zur Ausrichtung des Servos
            * min_pulse: Pulsdauer für Position ganz links
            * max_pulse: Pulsdauer für Position ganz rechts
        """
        super().__init__()

        self._servo = servo.Servo(pca.channels[pwmChannel], min_pulse=min_pulse, max_pulse=max_pulse)

    def update(self, vehicle):
        """
        Servo anhand der Fahrtichtung drehen. Die Fahrtrichtung wird als
        Zahl [-1...1] gesteuert und hier in einen Winkel von [10°-170°]
        umgerechnet.
        """
        self._servo.angle = (((vehicle.direction * -1) + 1) * 80) + 10

