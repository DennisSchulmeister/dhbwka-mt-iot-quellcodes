import collections, errno, json, socket, threading, time, traceback

class RemoteConnection:
    """
    Hintergrundthread zur Kommunikation mit dem Fahrzeug über UDP. Stellt auf Anforderung
    vom UI ein Verbindung zum Fahrzeug her, indem periodisch ein neuer Status vom Fahrzeug
    angefordert und die darauffolgende Antwort ausgewertet wird. Zusätzlich kann das UI
    verschiedene Befehle auslösen, die an das Fahrzeug gesendet werden.

    Innerhalb des UI sollten folgende Attribute mit Rückruffunktionen gesetzt werden:

      * on_connection_change(connected):
        Wird beim Herstellen oder Trennen der Verbindung aufgerufen. Das übergebene Flag
        teilt mit, ob eine Verbindung zum Fahrzeug besteht oder nicht.
    
      * on_receive_vehicle_status(vehicle_status):
        Wird beim Empfang neuer Fahrzeugdaten aufgerufen, um das UI zu aktualisieren.
        vehicle_status ist ein Dictionary mit den allgemeinen Fahrzeugparametern.

      * on_receive_sensor_status(sensor_status):
        Wird beim Empfang neuer Sensorinformationen aufgerufen, um das UI zu aktualisieren.
        sensor_status ist ein Dictionary mit einem Aktivkennzeichen je Sensorname.

      * on_receive_sound_status(sound_status):
        Wird beim Empfang neuer Statusinformationen des Audioplayers aufgerufen, um das UI
        zu aktualisieren. sound_status ist ein Dictionary mit den beiden Attributen soundfiles
        und playing. Beide beinhalten jeweils eine Liste mit den Namen der Audiodateien.
    """

    _BUFFER_SIZE = 4096
    
    def __init__(self, host, port, remote_port, update_frequency):
        """
        Konstruktor. Parameter:
            * host: Hostname, an den der UDP-Socket gebunden wird
            * port: Portnummer, an den der UDP-Socket gebunden wird
            * remote_port: Portnummer des UDP-Sockets auf dem Fahrzeug
            * update_frequency: Anzahl angefragter Aktualisierungen je Sekunde
        
        Wird für `host` ein leerer String übergeben, lauscht der UDP-Socket auf allen Adressen und
        allen Netzwerkschnittstellen.
        """
        self.on_connection_change      = None
        self.on_receive_vehicle_status = None
        self.on_receive_sensor_status  = None
        self.on_receive_sound_status   = None

        self._host             = host or None
        self._port             = port
        self._connected        = False
        self._remote_ip        = None
        self._remote_port      = remote_port
        self._timeout_s        = 1.0 / update_frequency
        self._pending_commands = collections.deque()

    def connect(self, remote_ip):
        """
        Vom UI-Thread aufgerufene Methode, um eine Verbindung mit dem Fahrzeug herzustellen.
        Startet lediglich den Netzwerk-Thread mit der eigentlichen Verbindungslogik, sofern
        dieser nicht sowieso schon läuft.
        """
        if self._connected:
            return

        self._remote_ip = remote_ip

        network_thread   = threading.Thread(target=self._network_thread_loop)
        network_thread.setDaemon(True)
        network_thread.start()

    def disconnect(self):
        """
        Vom UI-Thread aufgerufene Methode, um die Verbindung zum Fahrzeug zu trennen.
        Signalisiert lediglich dem Netzwerk-Thread, dass die Verbindung getrennt und
        der Thread beendet werden soll. Macht nichts, wenn keine Verbindung besteht.
        """
        if not self._connected:
            return
        
        self._pending_commands.append({"cmd": "_disconnect"})

    def send_set_attribute(self, attribute, value):
        """
        Vom UI-Thread aufgerufene Methode, um einen Fahrzeugparameter zu ändern.
        """
        self._pending_commands.append({"cmd": "set", "attr": attribute, "value": value})

    def send_enable_sensor(self, name, enabled):
        """
        Vom UI-Thread aufgerufene Methode, um einen Sensor ein- oder auszuschalten.
        """
        command = "enable_sensor" if enabled else "disable_sensor"
        self._pending_commands.append({"cmd": command, "name": name})

    def send_play_soundfile(self, soundfile, play):
        """
        Vom UI-Thread aufgerufene Methode, um die Wiedergabe eines Sounds zu starten
        oder zu stoppen.
        """
        command = "play_sound" if play else "stop_sound"
        self._pending_commands.append({"cmd": command, "name": soundfile})

    def _network_thread_loop(self):
        """
        Hauptschleife des Netzwerk-Threads. Sendet periodisch eine Statusanfrage an das Fahrzeug
        und verarbeitet die daraufhin empfangenen Antworten.
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
        
        self._connected = True
        self.on_connection_change(self._connected) if self.on_connection_change else None

        def _sendto(address, command):
            bytes = json.dumps(command).encode()

            for socket_ in sockets:
                try:
                    socket_.sendto(bytes, address)
                except Exception:
                    continue

        while self._connected:
            ## FIXME: Prüfen
            # Kleine Pause zur Entlastung der CPU
            time.sleep(self._timeout_s)

            # Statusanfragen und vom UI vorgemerkte Befehle an das Fahrzeug senden
            # FIXME: Deutliche Verbesserung der Latenz, indem nur alle Sekunden eine Anfrage an das Fahrzeug gesendet wird.
            #        Das Fahrzeug sendet daraufhin für die nächsten 15 Sekunden selbstständig einen periodischen Status.
            #        Netzwerklatenzen fallen dadurch nur noch zur Hälfte ins Gewicht.
            remote_address = (self._remote_ip, self._remote_port)

            _sendto(remote_address, {"cmd": "vehicle_status"})
            _sendto(remote_address, {"cmd": "sensor_status"})
            _sendto(remote_address, {"cmd": "sound_status"})

            while True:
                try:
                    command = self._pending_commands.pop()
                except IndexError:
                    break
                
                if command.get("cmd", "") == "_disconnect":
                    self._connected = False
                    continue
                
                _sendto(remote_address, command)

            # Antworten vom Fahrzeug empfangen und verarbeiten
            for socket_ in sockets:
                try:
                    # Neue Daten vom Socket empfangen und verarbeiten
                    data = socket_.recv(self._BUFFER_SIZE)
                    command = json.loads(data.decode())

                    if not "cmd" in command or not "data" in command:
                        continue

                    if command["cmd"] == "vehicle_status_response":
                        # Neue Fahrzeugparameter empfangen
                        if self.on_receive_vehicle_status:
                            self.on_receive_vehicle_status(command["data"])
                    elif command["cmd"] == "sensor_status_response":
                        # Neue Sensorinformationen empfangen
                        if self.on_receive_sensor_status:
                            self.on_receive_sensor_status(command["data"])
                    elif command["cmd"] == "sound_status_response":
                        # Neuer Soundstatus empfangen
                        if self.on_receive_sound_status:
                            self.on_receive_sound_status(command["data"])
                except OSError as err:
                    if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                        continue
                    else:
                        print(f"Socket-Fehler: {err}")
                        traceback.print_exc()
                except Exception as exc:
                    print(f"Fehler im Netzwerk-Thread: {exc}")
                    traceback.print_exc()

        for socket_ in sockets:
            try:
                socket_.close()
            except Exception as exc:
                print(f"Socket-Fehler: {exc}")
                traceback.print_exc()

        self.on_connection_change(self._connected) if self.on_connection_change else None