from carbot_sim.utils import clip

class Vehicle:
    """
    Klasse zur Steuerung des Fahrzeugs. Beinhaltet die Hauptschleife des
    Programms, in der mehrmals je Sekunde die Sensoren abgefragt und die
    Motorgeschwindigkeit entsprechend reguliert wird.
    """
    # Erkannte Fahrbahnmarkierung unter dem Fahrzeug.
    # Kann beim Selbstfahren ausgewertet werden, um einer Bodenlinie zu folgen.
    line_pattern: tuple[int] = (0,0,0,0,0)

    # Zielgeschwindigkeit [-1...1]: -1 = rückwärts, 1 = vorwärts
    target_speed: float = 0.0

    # Verlangsamung aufgrund von Hindernissen in der Fahrlinie [0...1]
    # Positive Werte werden bei Vorwärtsfahrt berücksichtigt, negative
    # Werte bei Rückwärtsfahrt
    obstacle_pushback: float = 0.0

    # Richtung [-1...1]: -1 = links, 0 = gerade aus, 1 = rechts
    direction: float = 0.0

    def __init__(self, motor_left, motor_right):
        """
        Konstruktor. Parameter:
            * motor_left: gpiozero.Motor-Objekt für den linken Fahrmotor
            * motor_right: gpiozero.Motor-Objekt für den rechten Fahrmotor
        """
        # Antriebsmotoren
        self._motor_left  = motor_left
        self._motor_right = motor_right

        self._speed_total = 0.0
        self._speed_left  = 0.0
        self._speed_right = 0.0
    
        # Tasks für die Fahrzeugfunktionen
        self._tasks = {}

    def add_task(self, name, task):
        """
        Fügt einen dauerhaft laufenden Task dem Fahrzeugobjekt hinzu und
        startet den Task.
        """
        self._tasks[name] = task
        
        if not task.task:
            task.run()
    
    def get_task(self, name):
        """
        Sucht einen Task anhand seines Namens. Wirft einen `KeyError`, wenn
        der Task nicht gefunden wurde.
        """
        return self._tasks[name]
    
    async def drive(self, update_frequency):
        """
        Task-Routine (genauer gesagt „asynchrone Co-Routine für einen Task”)
        zur Steuerung des Fahrzeugs. Dieser Task wertet die Fahrzeugparameter
        aus und übersetzt sie in Steueranweisungen für die Antriebsmotoren.

        Parameter:
            * update_frequency: UpdateFrequency-Objekt zur Bestimmung der Anzahl
              Kurskorrekturen je Sekunde
        """
        while True:
            # Task pausieren, damit andere Tasks auch laufen können
            await update_frequency.sleep()

            # Angestrebte Geschwindigkeit einstellen
            self._speed_total = clip(self.target_speed, -1, 1) - clip(self.obstacle_pushback, -1, 1)

            if self._speed_total > 0:
                self._speed_total = clip(self._speed_total, 0.4, 1)
            elif self._speed_total < 0:
                self._speed_total = clip(self._speed_total, -1, -0.4)

            # Einzelgeschwindigkeiten anpassen für Lenkung
            self._speed_left  = self._speed_total
            self._speed_right = self._speed_total

            if self._speed_total != 0:
                if self.direction > 0:
                    # Richtung rechts: Rechten Motor verlangsamen, damit sich das Fahrzeug dreht
                    self._speed_right *= 1 - self.direction
                elif self.direction < 0:
                    # Richtung links: Linken Motor verlangsamen, damit sich das Fahrzeug dreht
                    self._speed_left *= 1 + self.direction

            # Berechnete Motorgeschwindigkeiten übernehmen
            self._motor_left.value  = self._speed_left
            self._motor_right.value = self._speed_right