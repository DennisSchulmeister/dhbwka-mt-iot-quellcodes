"""
Python-Modul für das Einlesen und Verwalten von API-Keys.
"""

import json, os.path

class ApiKeyManager:
    """
    Simple Klasse zum Einlesen von API-Keys aus einer JSON-Datei. Die JSON-Datei muss
    hierfür folgenden Aufbau besitzen:

      {
        "service1": {
            "name1": "wert1",
            "name2": "wert2"
        },
        "service2": {
            "name": "wert"
        }
      }
    
    Es handelt sich dabei um ein JSON-Objekt, das für jeden Service ein weiteres
    Objekt als Attribut beinhaltet. Die Inhalte des inneren Objekts hängen dabei
    vom jeweiligen Service ab. Es obliegt dem Verwender der Klasse, vorzugeben,
    wie das innere Objekt strukturiert sein muss.

    Standardmäßig wird die Datei ../../API_KEY.json eingelesen. Der Pfad kann aber
    beim Instantiieren des Objekts übersteuert werden.
    """
    def __init__(self, filename="../../API_KEY.json"):
        """
        Konstruktor. Liest die Inhalte der übergebenen JSON-Datei ein. Wirft die
        typischen Ausnahmen, die beim Einlesen und Parsen einer JSON-Datei entstehen
        können, wenn die Datei nicht existiert oder fehlerhaft ist.
        """
        filename = os.path.normpath(filename)

        if filename.startswith("../") or filename.startswith("./"):
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, filename)
        
        with open(filename, "r") as api_key_file:
            self.apis = json.loads(api_key_file.read())

    def get(self, api):
        """
        Gibt die API-Keys eines bestimmten Services zurück. Liefert immer ein
        Dictionary zurück, selbst wenn der Service nicht gefunden wurde. In diesem
        Fall ist das Dictionary einfach leer.
        """
        if api in self.apis:
            return self.apis[api]
        else:
            return {}