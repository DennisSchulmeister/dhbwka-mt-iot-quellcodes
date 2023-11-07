import abc, asyncio, time

def clip(value, min_value, max_value):
    """
    Hilfsfunktion, die sicherstellt, dass das übergebene Wert innerhalb des angegebenen
    Bereichs bleibt.
    """
    return min(max(value, min_value), max_value)

class UpdateFrequency:
    """
    Hilfsobjekt zur Verwendung in den Tasks, die in einer festen Frequenz bestimmte Aktionen
    auslösen sollen. Indem diese Klasse für jeden Task einmalig instantiiert und dann in der
    Schleife des Tasks die Methode `sleep`aufgerufen wird, wird sichergestellt, dass die
    Aufgaben des Tasks immer im selben Zeitabstand ausgeführt werden.
    """
    
    def __init__(self, hz):
        """
        Konstruktor. Parameter:
            * hz: Anzahl der Taskaufrufe je Sekunde
        """
        self._target_delay_s = 1.0 / hz
        self._prev_time_s = 0.0
        self._needed_delay_s = 0.0
    
    async def sleep(self):
        """
        Aktuellen Task unterbrechen, um eine feste Update-Frequenz sicherzustellen.
        """
        self._current_time_s = time.monotonic()
        self._needed_delay_s = max(self._target_delay_s - (self._current_time_s - self._prev_time_s), 0.0)
        self._prev_time_s = self._current_time_s
        
        await asyncio.sleep(self._needed_delay_s)

class InfiniteTask(abc.ABC):
    """
    Abstrakte Basisklasse für eine Fahrzeugfunktion. Kapselt im Grunde genommen
    einen dauerhaft laufenden Task der auf Anweisung pausiert werden kann.
    """
    # Kennzeichen zur Pausierung der Funktion
    paused = False

    def __init__(self, update_frequency, vehicle):
        """
        Konstruktor. Muss von den erbenden Klassen aufgerufen werden.
        """
        self.task = None
        self.paused = False
        self._update_frequency = update_frequency
        self._vehicle = vehicle
    
    def run(self):
        """
        Hintergrundtask starten und darin in regelmäßigen Abständen die
        Methode `_update()` aufrufen, sofern der Task nicht pausiert wurde.
        """
        async def _coroutine():
            while True:
                await self._update_frequency.sleep()

                if not self.paused:
                    self._update(self._vehicle)

        self.task = asyncio.create_task(_coroutine())

    @abc.abstractmethod
    def _update(self, vehicle):
        """
        Von den Unterklassen zu überschreibende Methode. Hier beispielsweise die
        eigenen Sensordaten messen (wenn es nicht lange geht), die aktuellen
        Fahrparameter ermitteln und anpassen.
        """
        pass