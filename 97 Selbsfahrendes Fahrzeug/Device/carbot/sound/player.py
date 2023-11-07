import collections, os, shutil, subprocess
from carbot.sensors.base import SensorBase

class SoundPlayer(SensorBase):
    """
    Fahrzeugobjekt, mit dem einfache Soundfiles auf einem angeschlossenen Lautsprecher
    abgespielt werden können. Die Soundfiles müssen hierfür im Unterverzeichnis "media"
    abgelegt werden. Die Wiedergabe erfolgt mit dem Kommandozeilenprogramm aplay ohne
    zusätzliche Parameter. Dementsprechend erfolgt die Wiedergabe auf dem Standard Audio
    Device von ALSA, was normalerweiße der Kopfhöreranschluss des Raspberry Pi sein sollte.

    Die Methoden dieser Klasse sind threadsicher programmierung, so dass sie aus mehreren
    Threads parallel aufgerufen werden können, beispielsweise aus einem Serverthread, der
    Steuerbefehle über das Netzwerk empfängt. Die tatsächliche Wiedergabe wird dann in der
    update()-Methode im Hauptthread des Fahrzeugs ausgeführt.
    """

    def __init__(self, player="aplay", media_dir=None):
        """
        Konstruktor. Erlaubt die Wiedergabe mit folgenden Parametern zu beeinflussen:

         * player: Kommando zum Abspielen eines Soundfiles (Default: "aplay")
         * media_dir: Verzeichnis mit den Audiodateien (Default: Unterverzeichnis "media")
        """
        super().__init__()

        self._player    = shutil.which(player)
        self._media_dir = media_dir
        
        if not self._media_dir:
            self._media_dir = os.path.join(os.path.dirname(__file__), "media")
        
        self._pending_commands = collections.deque()
        self._player_processes = collections.deque()
    
    def update(self, vehicle):
        """
        Von SensorBase geerbte, abstrakte Methode. Hier werden die aus den anderen Threads
        empfangenen Befehle im Hauptthread des Fahrzeugs ausgeführt.
        """
        # Empfangene Befehle abarbeiten
        while True:
            try:
                command = self._pending_commands.pop()
            except IndexError:
                break
        
            if command["cmd"] == "play":
                self._play(command["soundfile"])
            elif command["cmd"] == "stop":
                self._stop(command["soundfile"])
        
        # Liste mit den laufenden Wiedergabeprogrammen aufräumen
        active_players = []

        for process in self._player_processes.copy():
            process.poll()

            if process.returncode == None:
                active_players.append(process)

        self._player_processes.clear()

        for process in active_players:
            self._player_processes.append(process)
    
    @property
    def soundfiles(self):
        """
        Gibt eine Liste mit den Namen der verfügbaren Soundfiles zurück. Diese können dann
        an die Methoden play() und stop() übergeben werden.
        """
        result = []

        with os.scandir(self._media_dir) as media_dir:
            for entry in media_dir:
                if entry.is_file():
                    result.append(entry.name)
        
        result.sort()
        return result

    @property
    def playing(self):
        """
        Gibt eine Liste mit den Namen der gerade wiedergegebenen Sounds zurück. Diese Methode
        kann aus beliebigen Threads aufgerufen werden.
        """
        result = [process._soundfile_ for process in self._player_processes.copy()]
        return result
    
    def play(self, soundfile):
        """
        Aus beliebigen Threads aufrufbare Methode, um die Wiedergabe eines Sounds anzufordern.
        """
        self._pending_commands.append({
            "cmd": "play",
            "soundfile": soundfile
        })
    
    def _play(self, soundfile):
        """
        Aufgerufen im Hauptthread des Fahrzeugs, um die Wiedergabe eines Sounds zu starten.
        """
        filename = os.path.join(self._media_dir, soundfile)
        process = subprocess.Popen([self._player, filename])

        if process.returncode == None:
            process._soundfile_ = soundfile
            self._player_processes.append(process)

    def stop(self, soundfile):
        """
        Aus beliebigen Threads aufrufbare Methode, um den Abbruch eines Sounds anzufordern.
        """
        self._pending_commands.append({
            "cmd": "stop",
            "soundfile": soundfile
        })
    
    def _stop(self, soundfile):
        """
        Aufgerufen im Hauptthread des Fahrzeugs, um die Wiedergabe eines Sounds zu stoppen.
        """
        for process in self._player_processes:
            process.poll()

            if process._soundfile_ == soundfile and process.returncode == None:
                process.terminate()
