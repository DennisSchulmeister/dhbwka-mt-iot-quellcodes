I-Paint: Der KI-Bildgenerator
=============================

Dieses Beispiel nutzt die öffentliche API des DALL-E Bildgenerators von OpenAI.
Es handelt sich um ein einfaches Programm, das nach einer Beschreibung des zu
erzeugenden Bildes fragt und das Bild anschließend im Browser öffnet.

 * DALL-E Weboberfläche: https://labs.openai.com/
 * API-Beschreibung: https://platform.openai.com/docs/guides/images

<p float="left">
  <img src="Beispielbilder/Astronaut%20with%20cowboy%20hat%20riding%20horse%20on%20Mars.png" width="200"/>
  <img src="Beispielbilder/Mad%20professor%20working%20late%20night%20on%20his%20computer.png" width="200"/>
  <img src="Beispielbilder/Oil%20painting%20of%20five%20dogs%20playing%20music%20instruments.png" width="200"/>
  <img src="Beispielbilder/Snoopy%20as%20Joe%20Cool%20leaning%20against%20his%20red%20dog%20house%2C%20garden%20and%20living%20houses%20in%20the%20background.png" width="200"/>
</p>

Vorbereitung
------------

Auf folgender Seite muss zunächst ein API-Key erzeugt werden:
https://platform.openai.com/api-keys

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

 * API-Key generieren: https://platform.openai.com/api-keys
 * Seite mit der Organisation-ID: https://platform.openai.com/account/organization
 * Verbleibendes Guthaben: https://platform.openai.com/usage

Ausführen des Beispiels
-----------------------

Dieses Projekt verwendet eine simple `requirements.txt`-Datei zur Deklaration
der benötigten Bibliotheken. Dies ist die einfachste Art, wie ein Python-Projekt
seine Abhängigkeiten definieren kann. Als Nutzer:in/Entwickler:in des Projekts
legt man sich dann einfach ein neues Python Environment an und installiert darin
mit folgenden Befehlen die Bibliotheken:

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