import time

def clip(value, min_value, max_value):
    """
    Hilfsfunktion, die sicherstellt, dass das übergebene Wert innerhalb
    des angegebenen Bereichs bleibt.
    """
    return min(max(value, min_value), max_value)

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
            * motor_left: gpiozero.Motor-ähnliches Objekt für den linken Fahrmotor
            * motor_right: gpiozero.Motor-ähnliches Objekt für den rechten Fahrmotor
        """
        # Antriebsmotoren
        self._motor_left  = motor_left
        self._motor_right = motor_right

        self._speed_total = 0.0
        self._speed_left  = 0.0
        self._speed_right = 0.0

        # Sonstige Sensoren und Aktoren
        self._sensors = []
        self._sensors_by_name = {}

    def add_sensor(self, name, sensor):
        """
        Fügt einen Sensor wie z.B. einen Abstandsmesser dem Fahrzeugobjekt
        hinzu. Der Sensor wird, sofern er aktiv ist, in der Hauptschleife
        abgefragt, um die Steuerungsparameter des Fahrzeugs anzupassen.
        """
        self._sensors.append(sensor)
        self._sensors_by_name[name] = sensor
    
    def get_sensor(self, name):
        """
        Sucht einen Sensor anhand seines Namens. Wirft einen `KeyError`, wenn
        der Sensor nicht gefunden wurde.
        """
        return self._sensors_by_name[name]
    
    @property
    def sensor_status(self):
        """
        Gibt ein Dictionary mit einem Flag je Sensor zurück, ob der jeweilige
        Sensor aktiv oder inaktiv ist.
        """
        sensor_status = {}

        for name in self._sensors_by_name.keys():
            sensor = self._sensors_by_name[name]

            if hasattr(sensor, "is_active"):
                sensor_status[name] = sensor.is_active
            else:
                sensor_status[name] = True

        return sensor_status

    def loop_forever(self, update_frequency=10):
        """
        Hauptschleife zur Steuerung des Fahrzeugs. Muss aufgerufen werden,
        damit das Fahrzeug regelmäßig seine Sensoren prüft und basierend
        auf den erhaltenen Werten die Antriebsmotoren ansteuert.

        Parameter:
            * update_frequency: Anzahl der Sensorprüfungen pro Sekunde.
        """
        target_delay_s = 1 / update_frequency
        prev_time_s = 0
        needed_delay_s = 0

        while True:
            # Thread pausieren, um CPU-Leistung einzusparen
            current_time_s = time.monotonic()
            needed_delay_s = target_delay_s - (current_time_s - prev_time_s)

            if needed_delay_s > 0:
                time.sleep(needed_delay_s)
            
            # Sensorwerte prüfen
            for sensor in self._sensors:
                if hasattr(sensor, "is_active"):
                    if not sensor.is_active:
                        continue
                
                if hasattr(sensor, "update"):
                    sensor.update(self)
            
            # Angestrebte Geschwindigkeit einstellen
            prev_speed_total = self._speed_total
            self._speed_total = clip(self.target_speed, -1, 1)
            
            if self.target_speed > 0 and self.obstacle_pushback > 0 \
            or self.target_speed < 0 and self.obstacle_pushback < 0:
                self._speed_total -= clip(self.obstacle_pushback, 0, 1)

            if self._speed_total > 0:
                self._speed_total = max(self._speed_total, 0.4)
            elif self._speed_total < 0:
                self._speed_total = min(self._speed_total, -0.4)

            # # Richtung umkehren, wenn einem Hinderniss ausgewichen wird
            # if prev_speed_total > 0 and self._speed_total < 0 \
            # or prev_speed_total < 0 and self._speed_total > 0:
            #     self.direction *= -1

            #     if self.direction >= -0.3 and self.direction <= 0.3:
            #         self.direction = clip(self.direction + 0.5, -1, 1)

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

            if self.obstacle_pushback != 0:
                # Richtung tauschen, wenn rückwärts einem Hinderniss ausgewichen wird
                self._speed_left *= -1
                self._speed_right *= -1
            
            # Berechnete Motorgeschwindigkeiten übernehmen
            self._motor_left.value  = self._speed_left
            self._motor_right.value = self._speed_right
    
    def stop(self):
        """
        Motoren stoppen bei Programmende.
        """
        self._motor_left.value  = 0
        self._motor_right.value = 0

    @property
    def speed_total(self):
        """
        Tatsächliche Gesamtgeschwindigkeit des Fahrzeugs. Kann von der
        Zielgeschwindigkeit abweichen, wenn Hindernisse in der Fahrlinie
        liegen.
        """
        return self._speed_total
    
    @property
    def speed_left(self):
        """
        Tatsächliche Geschwindigkeit des linken Motors.
        """
        return self._speed_left

    @property
    def speed_right(self):
        """
        Tatsächliche Geschwindigkeit des rechten Motors.
        """
        return self._speed_right
