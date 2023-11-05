import collections, errno, json, socket, threading, time, traceback
from carbot.sensors.base import SensorBase

# https://docs.python.org/3/library/socketserver.html#asynchronous-mixins
# https://wiki.python.org/moin/UdpCommunication
# https://pythontic.com/modules/socket/udp-client-server-example

# https://docs.python.org/3/library/collections.html#collections.deque
# https://docs.python.org/3/library/threading.html#lock-objects
# https://docs.python.org/3/library/json.html#module-json

class UDPRemoteControl(SensorBase):
    """
    Fernsteuerung des Fahrzeugs durch entfernte UDP-Clients. Startet einen Hintergrundthread,
    in dem ein UDP-Socket zum Empfangen von Steuerbefehlen geöffnet wird. Folgende Befehle
    werden dabei unterstützt:

        * Abruf der Fahrzeugparameter
        * Geschwindigkeit ändern
        * Richtung ändern
        * Vorhandene Sensoren abfragen
        * Sensor aktivieren/deaktivieren
        * Soundfile abspielen/stoppen
    
    Die Kommandos werden als UTF-8 kodiertes JSON-Objekt der Form `{"cmd": "...", ...}`
    übertragen, wobei auf die meisten Kommandos keine Antwort erfolgt.

    Kommandos ohne direkte Antwort:

        * `{"cmd": "set", "attr": "target_speed", "value": 0}`
        * `{"cmd": "set", "attr": "direction", "value": 0}`
        * `{"cmd": "enable_sensor", "name": "…"}`
        * `{"cmd": "disable_sensor", "name": "…"}`
        * `{"cmd": "play_sound", "name": "…"}`
        * `{"cmd": "stop_sound", "name": "…"}`
    
    Kommandos mit direkter Antwort:

        * `{"cmd": "vehicle_status"}`:
          liefert als Antwort ein Objekt mit den Fahrzeugparametern und ihren Werten.

        * `{"cmd": "sensor_status"}`:
          liefert als Antwort ein Objekt mit den Sensornamen und einem Aktiv-Flag.
        
        * `{"cmd": "sound_status"}`:
          liefert als Antwort ein Dictionary mit den beiden Attributen soundfiles
          und playing. Beide beinhalten jeweils eine Liste mit den Namen der Audiodateien.
    
    Die Nachrichten in beide Richtungen dürfen nicht größer als 4096 Bytes sein.
    """

    _BUFFER_SIZE = 4096
    _TIMEOUT_S = 0.05

    def __init__(self, host, port):
        """
        Konstruktor. Startet einen Server-Thread und öffnet darin einen UDP-Socket für die
        Abwicklung des entfernten Datenaustauschs.

        Parameter:
            * host: Hostname, an den der UDP-Socket gebunden wird
            * port: Portnummer, an den der UDP-Socket gebunden wird
        
        Wird für `host` ein leerer String übergeben, lauscht der Server auf allen Adressen und
        allen Netzwerkschnittstellen, wodurch er von entfernten Clients angesprochen werden kann.
        Wird stattdessen der Wert "localhost" oder eine IP-Adresse übergeben, kann der Server nur
        aus dem dazugehörigen IP-Netz (bei "localhost" also nur von der eigenen Maschine) erreicht
        werden.
        """
        super().__init__()

        self._host = host or None
        self._port = port

        self._pending_commands = collections.deque()
        self._vehicle_status   = {}
        self._sensor_status    = {}
        self._sound_player     = None
        self._available_sounds = []
        self._playing_sounds   = []
        self._status_lock      = threading.Lock()
        self._network_thread   = threading.Thread(target=self._network_thread_loop)

        self._network_thread.setDaemon(True)
        self._network_thread.start()
    
    def _network_thread_loop(self):
        """
        Hauptschleife des Netzwerk-Threads. Öffnet den UDP-Socket und bearbeitet die darüber empfangenen
        Kommandos. Anfragen nach dem Fahrzeugstatus werden anhand der letzten internen Kopie des
        Fahrzeugstatus direkt beantwortet. Alle anderen Anfragen werden in einer FIFO-Queue gesammelt
        und vom Fahrzeug-Thread bei nächster Gelegenheit abgearbeitet.
        """
        # Sockets öffnen sowohl für IPv6 als auch IPv4
        sockets = []

        # FIXME: Wirft OSError: [Errno 98] Address already in use, wenn IPv4 und IPv6 verwendet wird.
        # FIXME: Aktuell unklar, wie sowohl IPv4 als auch IPv6 unterstützt werden kann. Deshalb zunächst nur IPv4.
        # for address_info in socket.getaddrinfo(self._host, self._port, proto=socket.IPPROTO_UDP):
        #     try:
        #         socket_ = socket.socket(
        #             family = address_info[0],
        #             type   = address_info[1] | socket.SOCK_NONBLOCK,
        #             proto  = address_info[2]
        #         )
        #
        #         socket_.bind((self._host if self._host else "", self._port))
        #         sockets.append(socket_)
        #     except Exception as exc:
        #         print(f"Socket-Fehler: {exc}")
        #         traceback.print_exc()
        try:
            socket_ = socket.socket(
                family = socket.AF_INET,
                type   = socket.SOCK_DGRAM | socket.SOCK_NONBLOCK
            )

            socket_.bind((self._host if self._host else "", self._port))
            sockets.append(socket_)
        except Exception as exc:
            print(f"Socket-Fehler: {exc}")
            traceback.print_exc()
        
        # UDP-Pakete über die Sockets empfangen und verarbeiten
        sockets_without_data = 0

        while True:
            # FIXME: Prüfen
            if sockets_without_data == len(sockets):
                # Kleine Pause zur Entlastung der CPU, wenn kein Socket Daten liefert
                time.sleep(self._TIMEOUT_S)

            sockets_without_data = 0

            for socket_ in sockets:
                try:
                    # Neue Daten vom Socket empfangen und verarbeiten
                    data, address = socket_.recvfrom(self._BUFFER_SIZE)
                    command = json.loads(data.decode())

                    if not "cmd" in command:
                        continue

                    if command["cmd"] == "vehicle_status":
                        # Abfrage des Fahrzeugstatus direkt beantworten
                        # FIXME: Prüfen
                        # with self._status_lock:
                        response = json.dumps({"cmd": "vehicle_status_response", "data": self._vehicle_status})
                        socket_.sendto(response.encode(), address)
                    elif command["cmd"] == "sensor_status":
                        # Abfrage des Sensorstatus direkt beantworten
                        # FIXME: Prüfen
                        # with self._status_lock:
                        response = json.dumps({"cmd": "sensor_status_response", "data": self._sensor_status})
                        socket_.sendto(response.encode(), address)
                    elif command["cmd"] == "sound_status":
                        # Abfrage nach verfügbaren Soundfiles direkt beantworten
                        # FIXME: Prüfen
                        # with self._status_lock:
                        sound_status = {"soundfiles": self._available_sounds, "playing": self._playing_sounds}
                        response = json.dumps({"cmd": "sound_status_response", "data": sound_status})
                        socket_.sendto(response.encode(), address)
                    else:
                        # Alle anderen Steuerbefehle im Fahrzeug-Thread bearbeiten
                        self._pending_commands.append(command)
                except OSError as err:
                    if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                        sockets_without_data += 1
                        continue
                    else:
                        print(f"Socket-Fehler: {err}")
                        traceback.print_exc()
                except Exception as exc:
                    print(f"Fehler im Netzwerk-Thread: {exc}")
                    traceback.print_exc()

    def update(self, vehicle):
        """
        Im Fahrzeug-Thread regelmäßig aufgerufene Methode, in der der aktuelle Fahrzeugstatus ermittelt
        sowie das Fahrzeug gesteuert werden kann. Der aktuelle Fahrzeugstatus wird als internes Objekt
        zwischengespeichert, um Anfragen nach dem Status direkt im Server-Thread bearbeiten zu können.
        Anschließend werden die vom Server-Thread zwischenzeitlich gesammelten Steuerbefehle abgearbeitet.
        """
        # Aktuellen Fahrzeugstatus merken
        if self._status_lock.acquire(blocking=False):
            # Fahrzeugstatus ermitteln
            self._vehicle_status = {
                "line_pattern":      vehicle.line_pattern,
                "target_speed":      vehicle.target_speed,
                "obstacle_pushback": vehicle.obstacle_pushback,
                "direction":         vehicle.direction,
                "speed_total":       vehicle.speed_total,
                "speed_left":        vehicle.speed_left,
                "speed_right":       vehicle.speed_right,
            }

            self._sensor_status = vehicle.sensor_status.copy()
        
            # Soundplayer-Objekt merken und ggf. verfügbare Sounds einlesen, wenn der Player aktiviert wird
            if not self._sound_player:
                try:
                    sound_player = vehicle.get_sensor("sound:player")
                except KeyError:
                    sound_player = None

                if sound_player and sound_player.is_active:
                    self._sound_player     = sound_player
                    self._available_sounds = self._sound_player.soundfiles
                    self._playing_sounds   = self._sound_player.playing
            else:
                if self._sound_player.is_active:
                    self._playing_sounds = self._sound_player.playing
                else:
                    self._sound_player     = None
                    self._available_sounds = []
                    self._playing_sounds   = []

            # Sperre aufheben
            self._status_lock.release()
        
        # Empfangene Steuerbefehle verarbeiten
        while True:
            try:
                command = self._pending_commands.pop()
            except IndexError:
                break

            command_ = {
                "cmd":   command.get("cmd", ""),
                "attr":  command.get("attr", ""),
                "value": command.get("value", ""),
                "name":  command.get("name", ""),
            }
            
            if command_["cmd"] == "set" and command_["attr"] == "target_speed":
                # Zielgeschwindigkeit ändern
                try:
                    vehicle.target_speed = float(command_["value"])
                except ValueError:
                    pass
            elif command_["cmd"] == "set" and command_["attr"] == "direction":
                # Fahrtrichtung ändern
                try:
                    vehicle.direction = float(command_["value"])
                except ValueError:
                    pass
            elif command_["cmd"] == "enable_sensor":
                # Sensor aktivieren
                try:
                    sensor = vehicle.get_sensor(command_["name"])
                    sensor.enable()
                except:
                    pass
            elif command_["cmd"] == "disable_sensor":
                # Sensor deaktivieren
                try:
                    sensor = vehicle.get_sensor(command_["name"])
                    sensor.disable()
                except:
                    pass
            elif command_["cmd"] == "play_sound":
                if self._sound_player:
                    self._sound_player.play(command_["name"])
            elif command_["cmd"] == "stop_sound":
                if self._sound_player:
                    self._sound_player.stop(command_["name"])
