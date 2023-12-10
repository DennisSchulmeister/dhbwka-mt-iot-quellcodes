#! /usr/bin/env python
"""
Minimalbeispiel für ein typisches Python-Projekt. Zeigt die typische
Verzeichnisstruktur eines Python-Projekts und wie mit `python -m venv`
und `pip` ein isoliertes Environment aufgesetzt werden kann. Zum Test
wird hierfür von PyPi die Bibliothek `rich` installiert, um damit ein
farbiges Hello-World zu programmieren.
"""

import rich
from rich.prompt import Prompt

def main():
    """
    Hauptfunktion zum Starten des Programms.
    """
    name = Prompt.ask(
        "[bold bright_magenta]Wie heißt du?[/bold bright_magenta]",
        default="Dennis"
    )

    eis = Prompt.ask(
        "[bold bright_magenta]Welches ist dein Lieblingseis?[/bold bright_magenta]",
        choices = ["Schokolade", "Vanille", "Erdbeer"],
        default = "Erdbeer"
    )

    rich.print(f"Hallo, [red]{name}[/red]. Dein Lieblingseis ist [blue]{eis}[/blue]. :red_heart-emoji:\n")
