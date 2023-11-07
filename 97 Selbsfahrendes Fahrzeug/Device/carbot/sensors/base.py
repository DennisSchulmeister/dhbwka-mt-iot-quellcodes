import abc

class SensorBase(abc.ABC):
    """
    Abstrakte Basisklasse für einen Fahrzeugsensor, wobei das Wort „Sensor“ hier
    etwas irreführend ist. Denn Sensor meint hier nur, dass das Objekt innerhalb
    der Hauptschleife des Fahrzeugs aufgerufen wird und die Chance bekommt, die
    Fahrzeugparameter zu beeinflussen. Typischerweise indem die Klasse mit einem
    echten Sensor einen Wert misst und dann daraufhin Geschwindigkeit und Richtung
    des Fahrzeugs versucht zu ändern. Die Klasse kann stattdessen aber auch die
    Fahrparameter auslesen und mit einem Aktor eine Aktion auslösen.
    """
    is_active = True

    def __init__(self):
        """
        Konstruktor. Muss von den erbenden Klassen aufgerufen werden.
        """
        self.is_active = True
    
    def enable(self):
        """
        Sensor aktivieren, wenn er inaktiv war.
        """
        self.is_active = True
    
    def disable(self):
        """
        Sensor deaktivieren, wenn er aktiv war.
        """
        self.is_active = False
    
    @abc.abstractmethod
    def update(self, vehicle):
        """
        Verarbeitung während der Hauptschleife des Fahrzeugprogramms. Hier die eigenen
        Sensordaten messen (wenn es nicht lange geht), die aktuellen Fahrparameter
        ermitteln und ggf. anpassen.
        """
        pass
