Neues Python-Projekt
====================

 1. [Übersicht](#übersicht)
 1. [Abhängigkeiten verwalten mit venv](#abhängigkeiten-verwalten-mit-venv)
 1. [Probleme mit der PowerShell unter Windows](#probleme-mit-der-powershell-unter-windows)
 1. [Wichtige Pip-Kommandos](#wichtige-pip-kommandos)

Übersicht
---------

Dieses Beispiel zeigt den minimalen Aufbau eines typischen Python-Projekts.
Zwar schreibt Python keine sonderliche Struktur vor, ein paar einfache
Konventionen werden aber von den meisten Projekten eingehalten. Hierzu
zählen vor allem:

 * Verwendung von Pip oder anderen Tools zur Installation benötigter Bibliotheken
 * Installation der Bibliotheken in einem isolierten „Python Environment“
 * Eine README-Datei wie diese im Hauptverzeichnis des Projekts
 * Sonstige Konfigurationsdateien ebenfalls im Hauptverzeichnis des Projekts
 * Der eigentliche Quellcode je Programm in einem separaten Unterverzeichnis
 * Optional ein Startskript je Programm im Hauptverzeichnis oder einem `bin`-Unterverzeichnis
 * Weitere Verzeichnisse können Dokumentationen, Build-Pipelines uvm. beinhalten

Das Unterverzeichnis mit dem eigentlichen Python-Quellcode wird manchmal `src`
genannt. Öfters anzutreffen ist aber die Variante, bei der das Verzeichnis
wie das zu erstellende Programm heißt (hier `myapp`) und durch eine Datei
namens `__init__.py` als Python-Modul gekennzeichnet wurde. Denn dadurch
wird der Name des Verzeichnisses zum Prefix für alle programminternen Imports,
so dass Namenskonflikte mit externen Bibliotheken vermieden werden.

Abhängigkeiten verwalten mit venv
---------------------------------

Bei diesem Beispiel handelt es sich um eine typische Anwendung, die lediglich
eine Datei namens `requirements.txt` zur Definition der benötigten Bibliotheken
beinhaltet. Man geht davon aus, dass Entwickler und Nutzer der Anwendung schon
wissen, wie man damit ein isoliertes Environment aufsetzen und die Bibliotheken
darin installieren kann.

Die typischen Schritte sind die folgenden (Linux und Mac):

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Bzw. unter Windows (die zweite Zeile lautet hier anders):

```cmd
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

Die erste Zeile legt ein neues Environment im Unterverzeichnis `env` an.
Typischerweise wird dieses Verzeichnis in der Datei `.gitignore` von der
Versionierung mit Git ausgeschlossen, da es auf einem anderen Rechner
sowieso neu erzeugt werden muss.

Die zweite Zeile aktiviert das Environment in der aktuellen Konsolensitzung,
damit die dritte Zeile die in der `requirements.txt` definierten Abhängigkeiten
nicht systemweit sondern nur innerhalb des Environments installiert.

Ab jetzt kann die Anwendung gestartet werden; oder ein Python-Interpreter,
der ebenfalls nur auf die Bibliotheken des Environments zugreifen kann.
Zum Beispiel:

```sh
python
```

Oder:

```sh
python myapp.py
```

Mit `deactivate` kann das Environment deaktiviert werden. Alternativ kann
man natürlich auch einfach das Konsolenfenster schließen. :-) Will man zu
einem späteren Zeitpunkt wieder mit dem Environment arbeiten, muss es lediglich
vor dem Start von Python mit dem zweiten Befehl erneut aktiviert werden:

```sh
source env/bin/activate
```

Oder in der Kurzform (vgl. `man source`):

```sh
. env/bin/activate
```

Unter Windows lautet der Befehl hingegen:

```cmd
env\Scripts\activate
```

Alles Andere bleibt gleich.

Es bleibt übrigens einem selbst überlassen, ob man das Environment in einem Unterverzeichnis
des Projekts oder in irgend einem anderen Verzeichnis erzeugt. Wichtig ist nur, dass man für
jedes Projekt ein eigenes Environment anlegt, um die Abhängigkeiten sauber zu trennen.

Für eine sehr ausführliche Erklärung siehe:
https://realpython.com/python-virtual-environments-a-primer/

Probleme mit der PowerShell unter Windows
-----------------------------------------

Die Sicherheitseinstellungen von Windows verbieten die Ausführung von
PowerShell-Skripten, wenn dieses Feature nicht explizit aktiviert wurde.
Dies dient als Vorsorge gegen Skript-Viren, die bis in die frühen 2000er
ein großes Problem darstellten, schränkt die Gebrauchstauglichkeit der
PowerShell aber deutlich ein. Für uns heißt das aber leider auch, dass
die Aktivierung eines Environments zunächst mit folgender Fehlermeldung
abbricht:

  ```
  Die Datei "...\.env\Scripts\activate.ps1" kann nicht geladen werden, da
  die Ausführung von Skripts auf diesem System deaktiviert ist.
  ```

Indem die PowerShell einmal als Administrator geöffnet wird (einfach im
Startmenü nach PowerShell suchen und dann den entsprechenden Eintrag auswählen),
kann diese Richtlinie mit folgendem Befehl überprüft werden:

  ```PowerShell
  Get-ExecutionPolicy
  ```

Als Ergebnis wird in der Regel `restricted` angezeigt, was genau dem oben
beschriebenen Verhalten entspricht. Folgender Befehl ändert die Einstellung,
so dass signierte Skripte zugelassen werden:

  ```PowerShell
  Set-ExecutionPolicy RemoteSigned
  ```

Wichtige Pip-Kommandos
----------------------

Mit `pip` werden die abhängigen Bibliotheken verwaltet und installiert.
Hierfür werden folgende Befehle öfters benötigt:

 * Installation aller Abhängigkeiten: `pip install -r requirements.txt`
 * Installation einer einzelnen Bibliothek: `pip install bibliothek`
 * Deinstallation einer einzelnen Bibliothek: `pip uninstall bibliothek`
 * Anzeigen aller installierten Bibliotheken: `pip list`

Es ist allerdings zu beachten, dass die Installation oder Deinstallation
einer einzelnen Bibliothek, wie hier aufgeführt, nicht sinnvoll ist, wenn
es eine `requirements.txt`-Datei gibt. Denn die Datei wird durch die Befehle
nicht automatisch aktualisiert, so dass eine andere Person das Setup nicht
fehlerfrei nachstellen kann. Stattdessen sollte immer die Datei bearbeitet
und dann der erste Befehl zur Installation ausgeführt werden.
