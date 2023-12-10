#! /bin/env python
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
