I-Paint: Der KI-Bildgenerator
=============================

Dieses Beispiel nutzt die öffentliche API des DALL-E Bildgenerators von OpenAI.

 * DALL-E Weboberfläche: https://labs.openai.com/
 * API-Beschreibung: https://beta.openai.com/docs/guides/images
 * Tutorial auf Realpython.com: https://realpython.com/generate-images-with-dalle-openai-api/

<p float="left">
  <img src="Beispielbilder%2FAstronaut%20with%20cowboy%20hat%20riding%20horse%20on%20Mars.png" width="200"/>
  <img src="Beispielbilder/mad%20professor%20working%20late%20night%20on%20his%20computer.png" width="200"/>
  <img src="Beispielbilder%2FSnoopy%20as%20Joe%20Cool%20leaning%20against%20a%20red%20dog%20house.png" width="200"/>
  <img src="Beispielbilder/Astronaut%20with%20cowboy%20hat%20riding%20horse%20on%20Mars%20%282%29.png" width="200"/>
</p>

Varianten des Beispiels
-----------------------

 * **01 Minimalversion:** Super einfaches Python-Skript zum Aufruf der API
 * **02 Klassenbasierte Struktur:** Erste Zwischenversion auf dem Weg zu einer richtigen Anwendung
 * **03 Grafische Oberfläche:** Noch bessere Version, die zusätzlich ein Text UI besitzt

Die verschiedenen Versionen bauen aufeinander auf, wobei die erste Version nur
ein paar einfache Sprachfeatures von Python demonstrieren soll. Ab der zweiten
Version beginnt dann die *Überarbeitung zu einer richtigen Anwendung, die hierfür
sinnvoll in Klassen und Module gegliedert wurde. Die dritte Version baut darauf
auf und ersetzt das bis dahin sehr minimalistisch User Interface durch ein modernes
Text User Interface (eine Art GUI im Terminalfenster).

Vorbereitung
------------

Auf folgender Seite muss zunächst ein API-Key erzeugt werden:
https://beta.openai.com/account/api-keys

In diesem Verzeichnis muss dann eine Textdatei namens API_KEY.json angelegt werden,
in welcher der Key hineinkopiert werden muss. Die Datei wird nicht mit Git
versioniert und findet sich deshalb auch nicht auf GitHub. Der Inhalt muss wie
folgt aussehen:

  ```json
  {
    "openai": {
      "organization": "ID DER EIGENEN ORGANISATION",
      "api_key": "EIGENER API KEY"
    }
  }
  ```

 * API-Key generieren: https://beta.openai.com/account/api-keys
 * Seite mit der Organisation-ID: https://beta.openai.com/account/org-settings
 * Verbleibendes Guthaben: https://beta.openai.com/account/usage

Ausführen der Beispiele
-----------------------

Dieses Projekt verwendet eine simple `requirements.txt`-Datei zur Deklaration
der benötigten Bibliotheken. Dies ist die einfachste Art, wie ein Python-Projekt
seine Abhängigkeiten definieren kann. Als Nutzer/Entwickler des Projekts legt
man sich dann einfach ein neues Python Environment an und installiert darin mit
folgenden Befehlen die Bibliotheken:

__Linux/Mac:__

  ```sh
  python -m venv .env
  source env/bin/activate 
  pip install -r requirements.txt
  ```

__Windows:__

  ```sh
  python -m venv .env
  env\Scripts\activate
  pip install -r requirements.txt
  ```

Alternativ könnte mit einem Werkzeug wie Poetry eine Datei namens `pyproject.toml`
angelegt und verwaltet werden. Dies hätte den Vorteil, dass die Anwendung mit den
dafür vorgesehenen Werkzeugen von Python installiert werden kann, ohne manuell ein
Environment verwalten zu müssen. Für Bibliotheken, die in anderen Projekten verwendet
werden sollen, ist das besonders wichtig. Für einfache Programme wie dieses hier
aber nicht zwingend notwendig.