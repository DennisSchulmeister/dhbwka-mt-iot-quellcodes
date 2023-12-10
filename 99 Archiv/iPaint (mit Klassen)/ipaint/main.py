"""
Hauptdatei des Programms.
"""

from ipaint.apikey import ApiKeyManager
from ipaint.generator.openai import Text2Image_OpenAI_DallE

import os.path

def main():
    """
    Funktion mit der eigentlichen Programmlogik.
    """
    api_key_manager = ApiKeyManager()
    openai_api_key = api_key_manager.get("openai")

    openai_generator = Text2Image_OpenAI_DallE()
    openai_generator.set_api_key(openai_api_key)

    this_dir = os.path.dirname(__file__)
    save_dir = os.path.join(this_dir, "..", "..", "Beispielbilder")
    
    while True:
        prompt = input("Anfrage für zu generierendes Bild (zum Beenden leer lassen): ")
        prompt = prompt.strip()

        if not prompt:
            break
    
        print("Generiere Bild. Bitte warten ...")
    
        image = openai_generator.generate(prompt)
        image.open_browser()

        answer = input("Soll das Bild gespeichert werden? (J/N) [N] ")

        if answer.upper().strip() == "J":
            filename = image.download(save_dir)
            print(f"Bild wurde gespeichert: {os.path.relpath(filename, this_dir)}")
        
        print()
