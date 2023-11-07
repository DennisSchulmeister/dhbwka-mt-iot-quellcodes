#! /bin/env python
"""
Alternatives Beispiel für ein typisches Python-Projekt. Im Gegensatz
zum ersten Beispiel wird hier ein moderneres Werkzeug zur Verwaltung
der Abhängigkeiten und Environments verwendet: Poetry.

Poetry automatisiert die Erstellung und Verwendung eines isolierten
Python Environments vollständig. Auch kümmert es sich automatisch um
die Deklaration der Abhängigkeiten und bietet eigene Befehle, um diese
einem Projekt hinzuzfügen, zu installieren oder zu deinstallieren.
Für JavaScript-Umsteiger fühlt sich die Arbeit damit mehr wie von
Node.js gewohnt an. :-)

Dieses Beispiel verwendet die auf `rich` aufbauende Bibliothek `textual`,
um eine grafische Terminalanwendung zu erstellen. Denn textbasierte
User Interfaces sind spätestens seit den 2010ern gerade unter Entwicklern
besonders populär! Da wollen wir als angehende Python-Entwickler natürlich
mithalten können. Diese Anwendung kann daher sowohl mit der Tastatur als
auch mit der Maus bedient werden, obwohl sie komplett im Terminal läuft.

Der eigentliche Quellcode dieses Programms ist gar nicht so wichtig.
Er wurde einfach aus der Textual-Dokumentation geklaut und etwas
erweitert:

    https://textual.textualize.io/widgets/directory_tree/

Wichtig ist nur, dass es sich bei den importierten Klassen um keine
Standardklassen von Python handelt, sondern diese erst mit Poetry in
ein Python Environment installiert werden müssen, bevor die Anwendung
gestartet werden kann. Wie das geht steht im README-File.
"""

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Footer, Header

class DirectoryTreeApp(App):
    """
    Hauptklasse der Anwendung. Definiert das User Interface.
    """

    TITLE = "Hallo, Python!"

    BINDINGS = [
        ("x", "quit", "Programm beenden"),
        ("f", "toggle_dark", "Farbschema umschalten"),
    ]

    def compose(self) -> ComposeResult:
        """
        Von Textual vorgesehene Methode zum Erzeugen der UI-Widgets.
        """
        yield Header()
        yield Footer()
        yield DirectoryTree("./")

    def action_toggle_dark(self) -> None:
        """
        Footer-Aktion: Farbschema umschalten
        """
        self.dark = not self.dark

    def action_quit(self) -> None:
        """
        Footer-Aktion: Programm beenden
        """
        self.exit()

if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
