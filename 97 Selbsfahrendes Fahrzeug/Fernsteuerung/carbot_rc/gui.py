import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainWindow:
    """
    Hauptfenster der Anwendung.
    """

    def __init__(self, connection):
        """
        Konstruktor. Hier werden die tkinter-Widgets erstellt. Als Parameter muss ein zuvor
        erzeugte Instanz der Klasse RemoteConnection übergeben werden.
        """
        # Das Fenster selbst
        self._root = ttk.Window(title="Carbot Fernsteuerung", size=(1400, 540), resizable=(False, False))
        self._root.columnconfigure(1, weight=1)
        self._root.place_window_center()

        # Verbindung zum Fahrzeug
        connection_frame = self._create_row_frame(self._root, row=0, text="IP-Adresse", dark=True)
        connection_frame.columnconfigure(0, weight=1)
        
        self._remote_ip = tk.StringVar(value="192.168.178.121")
        self._remote_ip_entry = ttk.Entry(connection_frame, width=20, textvariable=self._remote_ip)
        self._remote_ip_entry.grid(row=0, column=1, sticky=(N,E,S,W))

        self._connect_button_text = tk.StringVar(value="Verbindung herstellen")
        self._connect_button = ttk.Button(connection_frame, textvariable=self._connect_button_text, bootstyle=PRIMARY, command=self._on_toggle_connection)
        self._connect_button.grid(row=0, column=2, sticky=(W))

        self._connected = False
        self._update_connection_widgets()

        # Sensoren
        self._sensor_frame = self._create_row_frame(self._root, row=1, text="Sensorstatus")
        self._sensor_widgets   = {}
        self._sensor_variables = {}
        self._sensor_status    = {}
        self._update_sensor_widgets()

        # Audiowiedergabe
        self._sound_frame = self._create_row_frame(self._root, row=2, text="Audiowiedergabe")
        self._sound_widgets   = {}
        self._sound_variables = {}
        self._sound_status    = {}
        self._update_sound_widgets()
        
        # Fahrzeugparameter        
        vehicle_frame = self._create_row_frame(self._root, row=3, text="Fahrzeugparameter")
        size_px = 200

        target_speed_meter = ttk.Meter(vehicle_frame, subtext="", amountused=0, textright="%", stripethickness=18, metersize=size_px, padding=6, bootstyle=PRIMARY)
        target_speed_meter.grid(row=0, column=0)
        target_speed_label = ttk.Label(vehicle_frame, text="target_speed")
        target_speed_label.grid(row=1, column=0)
        self._target_speed_value = target_speed_meter.amountusedvar
        self._target_speed_text  = target_speed_meter.labelvar

        self._obstacle_pushback = tk.DoubleVar()
        obstacle_pushback_scale = ttk.Scale(vehicle_frame, state=DISABLED, orient=VERTICAL, length=size_px, from_=-1.0, to=1.0, variable=self._obstacle_pushback, bootstyle=PRIMARY)
        obstacle_pushback_scale.grid(row=0, column=1)
        obstacle_pushback_label = ttk.Label(vehicle_frame, text="obstacle_pushback")
        obstacle_pushback_label.grid(row=1, column=1)

        speed_total = tk.DoubleVar()
        speed_total_meter = ttk.Meter(vehicle_frame, subtext="", amountused=0, textright="%", stripethickness=18, metersize=size_px, padding=6, bootstyle=INFO)
        speed_total_meter.grid(row=0, column=2)
        speed_total_label = ttk.Label(vehicle_frame, text="speed_total")
        speed_total_label.grid(row=1, column=2)
        self._speed_total_value = speed_total_meter.amountusedvar
        self._speed_total_text  = speed_total_meter.labelvar

        self._speed_left = tk.DoubleVar()
        speed_left_scale = ttk.Scale(vehicle_frame, state=DISABLED, orient=VERTICAL, length=size_px, from_=-1.0, to=1.0, variable=self._speed_left, bootstyle=INFO)
        speed_left_scale.grid(row=0, column=3)
        speed_left_label = ttk.Label(vehicle_frame, text="speed_left")
        speed_left_label.grid(row=1, column=3)

        self._speed_right = tk.DoubleVar()
        speed_right_scale = ttk.Scale(vehicle_frame, state=DISABLED, orient=VERTICAL, length=size_px, from_=-1.0, to=1.0, variable=self._speed_left, bootstyle=INFO)
        speed_right_scale.grid(row=0, column=4)
        speed_right_label = ttk.Label(vehicle_frame, text="speed_right")
        speed_right_label.grid(row=1, column=4)

        self._direction = tk.DoubleVar()
        direction_frame = ttk.Frame(vehicle_frame, padding=6)
        direction_frame.grid(row=2, column=0, pady=36)
        direction_scale = ttk.Scale(direction_frame, state=DISABLED, orient=HORIZONTAL, length=size_px, from_=-1.0, to=1.0, variable=self._direction, bootstyle=INFO)
        direction_scale.grid(row=0, column=0)
        direction_label = ttk.Label(direction_frame, text="direction")
        direction_label.grid(row=1, column=0)

        self._line_pattern = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        line_pattern_frame = ttk.Frame(vehicle_frame, padding=6)
        line_pattern_frame.grid(row=2, column=1, sticky=(N,E,S,W), pady=24)
        line_pattern_button1 = ttk.Checkbutton(line_pattern_frame, text="1", variable=self._line_pattern[0], state=DISABLED, bootstyle=(TOOLBUTTON, DANGER))
        line_pattern_button1.grid(row=0, column=0)
        line_pattern_button2 = ttk.Checkbutton(line_pattern_frame, text="2", variable=self._line_pattern[1], state=DISABLED, bootstyle=(TOOLBUTTON, DANGER))
        line_pattern_button2.grid(row=0, column=1)
        line_pattern_button3 = ttk.Checkbutton(line_pattern_frame, text="3", variable=self._line_pattern[2], state=DISABLED, bootstyle=(TOOLBUTTON, DANGER))
        line_pattern_button3.grid(row=0, column=2)
        line_pattern_button4 = ttk.Checkbutton(line_pattern_frame, text="4", variable=self._line_pattern[3], state=DISABLED, bootstyle=(TOOLBUTTON, DANGER))
        line_pattern_button4.grid(row=0, column=3)
        line_pattern_button5 = ttk.Checkbutton(line_pattern_frame, text="5", variable=self._line_pattern[4], state=DISABLED, bootstyle=(TOOLBUTTON, DANGER))
        line_pattern_button5.grid(row=0, column=4)
        line_pattern_label = ttk.Label(line_pattern_frame, text="line_pattern")
        line_pattern_label.grid(row=1, column=0, columnspan=5, pady=6)

        self._vehicle_status = {}
        self._update_vehicle_widgets()

        # Steuerfläche
        ttk.Label(vehicle_frame, padding=48).grid(row=0, column=5)
        vehicle_frame.columnconfigure(6, weight=1)
        self._control_canvas_size_px = 250
        self._control_marker_size_px = 9

        self._control_canvas = tk.Canvas(vehicle_frame)
        self._control_canvas.grid(row=0, column=6, rowspan=2, sticky=(N,E,S,W))
        self._control_canvas.bind("<Button-1>", self._on_control_canvas_click)
        self._control_canvas.bind("<B1-Motion>", self._on_control_canvas_click)
        self._control_canvas.bind("<ButtonRelease-1>", self._on_control_canvas_release)

        self._control_canvas.create_rectangle(0, 0, self._control_canvas_size_px, self._control_canvas_size_px, fill="#FFF0C0", outline="black")
        self._control_canvas.create_line(self._control_canvas_size_px / 2, 0, self._control_canvas_size_px / 2, self._control_canvas_size_px, fill="black")
        self._control_canvas.create_line(0, self._control_canvas_size_px / 2, self._control_canvas_size_px, self._control_canvas_size_px / 2, fill="black")

        self._control_canvas_marker = self._control_canvas.create_oval(
            (self._control_canvas_size_px / 2) - self._control_marker_size_px,
            (self._control_canvas_size_px / 2) - self._control_marker_size_px,
            (self._control_canvas_size_px / 2) + self._control_marker_size_px,
            (self._control_canvas_size_px / 2) + self._control_marker_size_px,
            fill="red", outline="black"
        )

        # Dummy zum Ausfüllen des Fensters nach unten
        self._root.rowconfigure(4, weight=1)
        self._create_row_frame(self._root, row=4)

        # Rückruffunktionen für die Klasse RemoteConnection registrieren
        self._connection = connection

        connection.on_connection_change      = self._on_connection_change
        connection.on_receive_vehicle_status = self._on_receive_vehicle_status
        connection.on_receive_sensor_status  = self._on_receive_sensor_status
        connection.on_receive_sound_status   = self._on_receive_sound_status
    
    def _create_row_frame(self, root, row, text="", dark=False):
        """
        Hilfsmethode zum Erzeugen eines Labels und Frames mit einer visuellen Zeile
        im Hauptfenster. Das Label befindet sich am linken Rand und hat einen dunklen
        Hintergrund. Der eigentliche Inhalt befindet sich rechts davon in einem Frame
        mit maximaler Breite und hellem Hintergrund.

        Parameter:
          * root: Elternelement
          * row: Zeile innerhalb des Elternelements, beginnend bei 0
          * text: Bezeichnung am linken Rand
          * dark: Flag für dunkleren Hintergrund
        
        Rückgabe: Frame für den eigentlichen Inhalt
        """
        ttk.Label(root, text=text, bootstyle=(INVERSE, DARK), padding=(6,6,24,6)).grid(row=row, column=0, sticky=(N,E,S,W))

        frame = ttk.Frame(root, bootstyle=SECONDARY if dark else DEFAULT, padding=6)
        frame.grid(row=row, column=1, sticky=(N,E,S,W))

        return frame

    # -----------------------
    # Verbindung zum Fahrzeug
    # -----------------------
    def _on_toggle_connection(self):
        """
        Klick auf den Button zum Herstellen oder Trennen der Verbindung.
        """
        if not self._connected:
            remote_ip = self._remote_ip.get()
            self._connection.connect(remote_ip)
        else:
            self._connection.disconnect()

    def _on_connection_change(self, connected):
        """
        Vom Netzwerk-Thread aufgerufene Rückruffunktion zur Aktualisierung des UIs nach
        einer Änderung des Verbindungsstatus.
        """
        def _in_ui_thread():
            self._connected = connected
            self._update_connection_widgets()

            if not connected:
                self._sensor_status = {}
                self._update_sensor_widgets()

                self._sound_status = {}
                self._update_sound_widgets()

                self._vehicle_status = {}
                self._update_vehicle_widgets()

        self._root.after_idle(_in_ui_thread)

    def _update_connection_widgets(self):
        """
        Widgets zur Verbindung mit dem Fahrzeug aktualisieren.
        """
        if self._connected:
            self._remote_ip_entry.configure(state=DISABLED)

            self._connect_button_text.set("Verbindung trennen")
            self._connect_button.configure(bootstyle=DANGER)
        else:
            self._remote_ip_entry.configure(state="")

            self._connect_button_text.set("Verbindung herstellen")
            self._connect_button.configure(bootstyle=PRIMARY)

    # --------
    # Sensoren
    # --------
    def _on_receive_sensor_status(self, sensor_status):
        """
        Vom Netzwerk-Thread aufgerufene Rückruffunktion zur Aktualisierung des UIs nach
        dem Empfang neuer Sensorinformationen.
        """
        def _in_ui_thread():
            self._sensor_status = sensor_status
            self._update_sensor_widgets()

        self._root.after_idle(_in_ui_thread)

    def _update_sensor_widgets(self):
        """
        Widgets für den Sensorstatus aktualisieren.
        """
        sensors = list(self._sensor_status)
        sensors.sort()

        rebuild_widgets = False
        if not sensors:
            rebuild_widgets = True

        for sensor in sensors:
            if not sensor in self._sensor_widgets:
                rebuild_widgets = True
                break
        
        if rebuild_widgets:
            for widget in self._sensor_widgets.values():
                widget.grid_remove()

            self._sensor_widgets   = {}
            self._sensor_variables = {}
            column = -1

            for sensor in sensors:
                def _create_widget(sensor):
                    def _callback(*args, **kwargs):
                        self._connection.send_enable_sensor(sensor, variable.get() == 1)

                    nonlocal column
                    column += 1

                    variable = tk.IntVar()
                    widget = ttk.Checkbutton(self._sensor_frame, text=sensor, variable=variable, command=_callback, bootstyle="round-toggle", padding=6)
                    widget.grid(row=0, column=column, sticky=(N,E,S,W), padx=6)

                    self._sensor_widgets[sensor] = widget
                    self._sensor_variables[sensor] = variable
                
                _create_widget(sensor)
        
        for sensor in sensors:
            variable = self._sensor_variables[sensor]
            active = self._sensor_status[sensor]
            variable.set(1 if active else 0)

    # ---------------
    # Audiowiedergabe
    # ---------------
    def _on_receive_sound_status(self, sound_status):
        """
        Vom Netzwerk-Thread aufgerufene Rückruffunktion zur Aktualisierung des UIs nach
        dem Empfang neuer Statusinformationen des Audioplayers.
        """
        def _in_ui_thread():
            self._sound_status = sound_status
            self._update_sound_widgets()

        self._root.after_idle(_in_ui_thread)

    def _update_sound_widgets(self):
        """
        Widgets für die Audiowiedergabe aktualisieren.
        """
        if "soundfiles" in self._sound_status:
            soundfiles = list(self._sound_status["soundfiles"])
            soundfiles.sort()
        else:
            soundfiles = []

        rebuild_widgets = False
        if not soundfiles:
            rebuild_widgets = True

        for soundfile in soundfiles:
            if not soundfile in self._sound_widgets:
                rebuild_widgets = True
                break
        
        if rebuild_widgets:
            for widget in self._sound_widgets.values():
                widget.grid_remove()

            self._sound_widgets   = {}
            self._sound_variables = {}
            column = -1

            for soundfile in soundfiles:
                def _create_widget(soundfile):
                    def _callback(*args, **kwargs):
                        if not args:
                            # Mausklick, ändert die Variable
                            self._connection.send_play_soundfile(soundfile, variable.get() == 1)
                        else:
                            # Tastatur, ändert die Variable nicht
                            self._connection.send_play_soundfile(soundfile, variable.get() == 0)

                    nonlocal column
                    column += 1
                    key = column + 1

                    if key < 10:
                        text = f"[{key}] {soundfile}"
                        key  = f"<KP_{key}>"
                    else:
                        text = soundfile
                        key  = None

                    variable = tk.IntVar()
                    widget = ttk.Checkbutton(self._sound_frame, text=text, variable=variable, command=_callback, bootstyle=TOOLBUTTON, padding=6)
                    widget.grid(row=0, column=column, sticky=(N,E,S,W), padx=6)

                    if key:
                        self._root.bind(key, _callback)

                    self._sound_widgets[soundfile] = widget
                    self._sound_variables[soundfile] = variable
                
                _create_widget(soundfile)
        
        if "playing" in self._sound_status:
            playing = self._sound_status["playing"]
        else:
            playing = []

        for soundfile in self._sound_widgets:
            variable = self._sound_variables[soundfile]
            variable.set(1 if soundfile in playing else 0)

    # -----------------
    # Fahrzeugparameter
    # -----------------
    def _on_receive_vehicle_status(self, vehicle_status):
        """
        Vom Netzwerk-Thread aufgerufene Rückruffunktion zur Aktualisierung des UIs nach
        dem Empfang neuer Fahrzeugparameter.
        """
        def _in_ui_thread():
            self._vehicle_status = vehicle_status
            self._update_vehicle_widgets()

        self._root.after_idle(_in_ui_thread)

    def _update_vehicle_widgets(self):
        """
        Widgets für die Fahrzeugdaten aktualisieren.
        """
        target_speed = int(self._vehicle_status.get("target_speed", 0) * 100)
        self._target_speed_value.set(abs(target_speed))
        self._target_speed_text.set("vorwärts" if target_speed >= 0 else "rückwärts")

        speed_total = int(self._vehicle_status.get("speed_total", 0) * 100)
        self._speed_total_value.set(abs(speed_total))
        self._speed_total_text.set("vorwärts" if speed_total >= 0 else "rückwärts")

        self._obstacle_pushback.set(self._vehicle_status.get("obstacle_pushback", 0))
        self._direction.set(self._vehicle_status.get("direction", 0))
        self._speed_left.set(self._vehicle_status.get("speed_left", 0))
        self._speed_right.set(self._vehicle_status.get("speed_right", 0))

        line_pattern = self._vehicle_status.get("line_pattern", [])
        for i in range(len(line_pattern)):
            self._line_pattern[i].set(line_pattern[i])

    # ------------
    # Steuerfläche
    # ------------

    def _on_control_canvas_click(self, event):
        """
        Fahrzeugparameter bei Klick auf die Steuerfläche ändern.
        """
        if not self._connected:
            return
        
        if event.x < 0:
            event.x = 0
        if event.x > self._control_canvas_size_px:
            event.x = self._control_canvas_size_px

        if event.y < 0:
            event.y = 0
        if event.y > self._control_canvas_size_px:
            event.y = self._control_canvas_size_px

        self._control_canvas.coords(
            self._control_canvas_marker,
            event.x - self._control_marker_size_px,
            event.y - self._control_marker_size_px,
            event.x + self._control_marker_size_px,
            event.y + self._control_marker_size_px,
        )

        target_speed = -1.0 * (event.y - self._control_canvas_size_px / 2) / (self._control_canvas_size_px / 2)
        direction = (event.x - self._control_canvas_size_px / 2) / (self._control_canvas_size_px / 2)

        self._connection.send_set_attribute("target_speed", target_speed)
        self._connection.send_set_attribute("direction", direction)
    
    def _on_control_canvas_release(self, event):
        """
        Fahrzeug stoppen, wenn die Maus losgelassen wird.
        """
        if not self._connected:
            return
        
        self._control_canvas.coords(
            self._control_canvas_marker,
            (self._control_canvas_size_px / 2) - self._control_marker_size_px,
            (self._control_canvas_size_px / 2) - self._control_marker_size_px,
            (self._control_canvas_size_px / 2) + self._control_marker_size_px,
            (self._control_canvas_size_px / 2) + self._control_marker_size_px,
        )

        self._connection.send_set_attribute("target_speed", 0.0)
        self._connection.send_set_attribute("direction", 0.0)

    # --------------------
    # Öffentliche Methoden
    # --------------------
    def mainloop(self):
        """
        Blockierende Methode zur Ausführung der tkinter "Hauptschleife". Diese Methode
        muss nach Erzeugung des Objekts aufgerufen werden, damit die Anwendung auf
        Ereignisse reagieren kann. Die Methode wird erst beendet, wenn das Programm
        beendet werden soll.
        """
        self._root.mainloop()