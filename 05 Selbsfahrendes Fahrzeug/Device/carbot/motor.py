from gpiozero import DigitalOutputDevice

class PCA9685Motor:
    """
    Hilfsklasse zur Steuerung eines Motors in Anlehnung an `gpiozero.Motor`.
    Da die Pulsweitenmodulation hier nicht vom Raspberry Pi sondern über einen
    externen PCA9685-Baustein gesteuert wird, ist es am einfachstn, eine eigene
    Klasse zur Ansteuerung eines Motors zu schreiben und sich bei der Schnittstelle
    an `gpiozero.Motor` zu orientieren.

    Auf Hardwarebene funktioniert die Ansteuerung wie folgt:

        * Jeder Motor ist mit zwei GPIO-Ausgängen verbunden, welche die Drehrichtung
          steuern. Der eine Pin signalisiert dem Motor Vorwärtsfahrt, der andere Pin
          Rückwärtsfahrt. Dementsprechend muss immer genau einer der beiden Pins aktiv
          sein, damit der Motor fahren kann. Beide Pins aktiv oder beide Pins inaktiv
          bedeutet Stopp.
    
        * Zusätzlich erhält jeder Motor über den PCA9685-Baustein ein PWM-Signal zur
          Steuerung der Geschwindigkeit.
    
    Geschwindigkeit und Richtung des Motors können mit dieser Klasse wie folgt
    geändert werden:

        * Methode `forward(0.0 ... 1.0)`: Vorwärtsfahrt
        * Methode `backward(0.0 ... 1.0)`: Rückwärtsfahrt
        * Methode `reverse()`: Fahrtrichtung umkehren
        * Methode `stop()`: Anhalten
        * Zuweisung an Attribut `value` = -1.0 ... 1.0
    """
    def __init__(self, pca, forward, backward, pwmChannel):
        """
        Konstruktor.

            * pca: PCA9685-Objekt für die PWM-Steuerung
            * forward: Nummer des GPIO-Pins für Vorwärtsfahrt
            * backward: Nummer des GPIO-Pins für Rückwärtsfahrt
            * pwmChannel: Nummer des PWM-Kanals für die Geschwindigkeitsregelung
        """
        self._forward    = DigitalOutputDevice(forward)
        self._backward   = DigitalOutputDevice(backward)
        self._pwmChannel = pca.channels[pwmChannel]
        self._value      = 0
    
    def forward(self, speed):
        """
        Motor in angegebener Geschwindigkeit vorwärts laufen lassen.
        """
        self.value = speed
    
    def backward(self, speed):
        """
        Motor in angegebener Geschwindigkeit rückwärts laufen lassen.
        """
        self.value = speed * -1
    
    def stop(self):
        """
        Motor anhalten.
        """
        self.value = 0
    
    def is_active(self):
        """
        Gibt True zurück, wenn der Motor läuft, sonst False.
        """
        return self.value != 0
    
    @property
    def value(self):
        """
        Auslesen der Richtung und Geschwindigkeit des Motors [-1...1]
        Negative Zahlen = Rückwärts, positive Zahlen = Vorwärts.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        """
        Richtung und Geschwindigkeit des Motors ändern durch einfache
        Wertzuweiseung statt Aufruf der obigen Methoden.
        """
        self._value = value
        self._pwmChannel.duty_cycle = int(0xFFFF * abs(value))

        if value > 0:
            self._forward.on()
            self._backward.off()
        elif value < 0:
            self._forward.off()
            self._backward.on()
        else:
            self._forward.off()
            self._backward.off()