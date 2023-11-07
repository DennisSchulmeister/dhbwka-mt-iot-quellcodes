"""
Abstrakte Basisklassen für das generator-Modul. In Python ist es zwar überhaupt
nicht notwendig, zwei gleichartige Klassen von einer gemeinsamen Basisklasse
erben zu lassen. Die Definition einer abstrakten Basisklasse hilft aber, die
erwartete Schnittstelle und ihre Implementierung zu dokumentieren.
"""

import abc, datetime, os.path, urllib.request, webbrowser

class Text2Image(abc.ABC):
    """
    Abstrakte Basisklasse für einen Text2Image Bildgenerator. Definiert die Schnittstelle,
    die jedes Objekt zur Erzeugung eines Bildes anhand einer Textbeschreibung implementieren
    muss. Darüber hinaus stellt sie ein paar allgemeine Methoden zur Verfügung, die immer
    denselben Quellcode besitzen.
    """
    def __init__(self):
        """
        Konstruktor.
        """
        self._api_key = {}

    def set_api_key(self, api_key):
        """
        API-Key des Services in `self._api_key` ablegen.
        """
        self._api_key = api_key
    
    @abc.abstractmethod
    def generate(self, prompt):
        """
        Methode zum Aufrufen der Bildgenerierung. Bekommt einen String mit der Anfrage
        des Anwenders übergeben und muss ein GeneratedImage-Objekt zurückliefern.
        """
        pass

class GeneratedImage:
    """
    Ein Objekt von dieser Klasse muss in der `generate()`-Methode eines Text2Image-
    Generators erzeugt und zurückgegeben werden. Der Aufrufer der Methode kann das
    Objekt dann verwenden, um das generierte Bild im Browser zu öffnen oder in einer
    lokalen Datei zu speichern.
    """
    def __init__(self, prompt, url, extension):
        """
        Konstruktor. Bekommt den ursprünglichen Anfragetext des Anwenders sowie die
        URL des daraus generierten Bildes übergeben. Zusätzlich wird die Dateiendung
        (z.B. "png") benötigt.
        """
        self._prompt = prompt
        self._url = url
        self._extension = extension

    def download(self, dirname):
        """
        Speichert ein zuvor mit einem Text2Image-Generator erzeugtes Bild als lokale
        Datei. Ist nicht die beste Implementierung, reicht aber. Gibt den Pfad der
        gespeicherten Datei zurück.
        """
        timestamp = datetime.datetime.now()
        filename = os.path.join(dirname, f"{self._prompt} {timestamp}.{self._extension}")
        filename = os.path.normpath(filename)

        with open(filename, "wb") as outfile:
            with urllib.request.urlopen(self._url) as response:
                outfile.write(response.read())
        
        return filename

    def open_browser(self):
        """
        Öffnet ein neues Browserfenster zur Anzeige der übergebenen Bild-URL. Die URL
        sollte zuvor mit einem Text2Image-Generator erzeugt worden sein.
        """
        webbrowser.open(self._url)