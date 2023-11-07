"""
Hauptdatei des Programms.
"""
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, TextLog

from ipaint.apikey import ApiKeyManager
from ipaint.generator.openai import Text2Image_OpenAI_DallE

import os.path

class IPaintApp(App):
    """
    Hauptklasse der Anwendung. Definiert das User Interface und nutzt die anderen
    Klassen der Anwendung zur Ausführung der gewünschten Aktionen.
    """

    CSS_PATH = "style.css"
    TITLE = "I-Paint (so therefor I am)"

    BINDINGS = [
        ("x", "quit", "Programm beenden"),
    ]

    _prompt = "Pyramid made of cheeseburgers, 1960s advertisement"
    _image = None
    _textlog = TextLog(id="textlog")

    def __init__(self):
        """
        Konstruktor. Erzeugt die internen Objekte zum Ansteuern des
        Text2Image-Generators.
        """
        super().__init__()

        api_key_manager = ApiKeyManager()
        openai_api_key = api_key_manager.get("openai")

        self._openai_generator = Text2Image_OpenAI_DallE()
        self._openai_generator.set_api_key(openai_api_key)

        self._this_dir = os.path.dirname(__file__)
        self._save_dir = os.path.join(self._this_dir, "..", "..", "Beispielbilder")

    def on_mount(self):
        """
        Von Textual vorgesehene Methode für Initialisierungen bei Erzeugung
        der Benutzeroberfläche.
        """
        self.dark = False

    def compose(self):
        """
        Von Textual vorgesehene Methode zum Erzeugen der UI-Widgets.
        """
        yield Header()
        yield Footer()
        yield Vertical(
            Input(placeholder="Zu generierendes Bild", value=self._prompt),
            Horizontal(
                Button("Generieren", id="generate", variant="primary"),
                Button("Anzeigen", id="display"),
                Button("Speichern", id="save"),
                id="buttons"
            ),
            self._textlog,
        )

    def on_input_changed(self, event):
        """
        Event Handler für Texteingaben im Einggabefeld.
        """
        self._prompt = event.value

    def action_quit(self):
        """
        Footer-Aktion: Programm beenden
        """
        self.exit()

    def on_button_pressed(self, event):
        """
        Event Handler für die Buttons.
        """
        self._textlog.clear()

        match event.button.id:
            case "generate":
                self._image = self._openai_generator.generate(self._prompt)
                self._textlog.write("Bild wurde erzeugt.")
            case "display":
                if self._image:
                    self._image.open_browser()
                    self._textlog.write("Browser wurde geöffnet.")
                else:
                    self._textlog.write("Generieren Sie erst ein Bild!")
            case "save":
                if self._image:
                    filename = self._image.download(self._save_dir)
                    filename = os.path.relpath(filename, self._this_dir)
                    self._textlog.write(f"Bild wurde gespeichert: {filename}")
                else:
                    self._textlog.write("Generieren Sie erst ein Bild!")
