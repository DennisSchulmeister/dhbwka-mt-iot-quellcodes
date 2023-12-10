Neues Python-Projekt mit Poetry
===============================

Übersicht
---------

Dies ist eine Abwandlung des vorherigen Beispiels zum typischen Aufbau
eines typischen Python-Projekts. Im Gegensatz zum Beispiel davor verwendet
diese Variante modernere Werkzeuge zur Verwaltung des Python Environments.
Zwar gehört die Verwendung isolierter Environments schon lange zu den Best
Practices in Python. In den letzten Jahren haben sich die Werkzeuge dafür
aber sehr weiterentwickelt.

Anstelle dem traditionellen Ansatz mit `python -m venv …` verwendet dieses
Projekt den [Poetry](https://python-poetry.org) Paketmanager. Dieser muss
allerdings separat installiert werden, da er nicht im Lieferumfang von
Python enthalten ist. Linux-Anwender haben hier meist Glück und können
die Paketverwaltung ihrer Distribution verwenden. Alle weniger Glücklichen
befolgen die [Installationsanweisungen auf der Poetry-Webseite](https://python-poetry.org/docs/#installation).

Die Konventionen zur Verzeichnisstruktur des Projekts sind nahezu gleich
geblieben. Lediglich das manuell verwaltete Verzeichnis `env` für das
Python Environment entfällt:

 * Eine README-Datei wie diese im Hauptverzeichnis des Projekts
 * Sonstige Konfigurationsdateien ebenfalls im Hauptverzeichnis des Projekts
 * Der eigentliche Quellcode je Programm in einem separaten Unterverzeichnis
 * Optional ein Startskript je Programm im Hauptverzeichnis oder einem `bin`-Unterverzeichnis
 * Weitere Verzeichnisse können Dokumentationen, Build-Pipelines uvm. beinhalten

Anstelle der bisherigen Datei `requirements.txt` tritt nun allerdings die Datei
`pyproject.toml`, die neben den Abhängigkeiten auch weitere Konfigurationen
rund um das Projekt beinhaltet.

Zusätzlich geht Poetry automatisch davon aus, dass jedes Programm in einem
Unterverzeichnis mit dem Namen des Programms und einer `__init__.py`-Datei
liegt. Außerdem legt es ein `test`-Verzeichnis für Unit Tests an, was im
letzten Beispiel nicht gemacht wurde, da es für diese einfache Anwendung
sowieso keine sinnvollen Unit Tests gibt.

Abhängigkeiten verwalten mit Poetry
-----------------------------------

### Neues Projekt anlegen

Zunächst muss ein neues Python-Projekt angelegt werden. Dies erledigt
der folgende Befehl, so dass die Verzeichnisstruktur nicht von Hand
erzeugt werden muss:

```sh
poetry init projektname
cd projektname
```

Anschließend können dem Projekt ganz einfach Bibliotheken hinzugefügt
oder entfernt werden. Poetry legt hierfür automatisch außerhalb des
Projektverzeichnisses ein Python Environment an, nimmt die entsprechenden
Installationsschritte darin vor und passt die Datei `pyproject.toml` an:

```sh
poetry add bibliothek
poetry remove bibliothek
```

### Vorhandenes Projekt verwenden

Falls das Python Environment gelöscht wird, oder man den Quellcode von einem
anderen Entwickler z.B. aus GitHub übernimmt, können die in der `pyproject.toml`
eingetragenen Abhängigkeit mit folgendem Befehl nachinstalliert werden. Auch
hierfür legt Poetry automatisch ein Environment an:

```sh
peotry install
```

Die installierten Bibliotheken zeigt folgender Befehl:

```sh
poetry show
```

Zum Start der Anwendung gibt es zwei Möglichkeiten: Entweder man verwendet
auch hierfür das `poetry`-Kommando, oder man aktiviert das Python Environment
vor der ersten Ausführung von Python. Variante 1 sieht so aus:

```sh
poetry run python dirtree.py
```

Oder unter Linux und Mac auch:

```sh
poetry run ./dirtree.py
```

Denn `peotry run` führt einfach nur den angehängten Befehl aus und stellt
dabei sicher, dass das Python Environment aktiv ist. Um sich die Tipparbeit
zu sparen, kann aber auch ganz einfach eine neue Shell mit bereits aktiviertem
Environment gestartet werden:

```sh
peotry shell
```

In dieser kann dann wie gewohnt Python ausgeführt werden. Mit `exit` wird
die Umgebung wieder verlassen.

Wichtiger Hinweis zu venv
-------------------------

Beim Ausprobieren der Beispiele kann es schnell passieren, dass man noch
das Environment aus der ersten Version aktiv hat und darin Poetry zu
Installation weiterer Bibliotheken ausführt. Dies hat dann leider den
unschönen Effekt, dass das noch aktive Environment verändert und kein neues
Environment für das zweite Beispielprojekt erzeugt wird. Sicherheitshalber
sollte man vor Ausprobieren der Beispiele den Befehl `deactivate` ausführen,
um ein eventuell noch aktives Python-Environment zu verlassen.
