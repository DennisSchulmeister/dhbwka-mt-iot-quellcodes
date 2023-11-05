#! /usr/bin/env python3

import json, os, webbrowser
import openai
#import pysnooper

#@pysnooper.snoop()
def main():
    """
    Funktion mit der eigentlichen Programmlogik.
    """
    # API-Key einlesen
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "..", "..", "API_KEY.json")

    with open(file_path, "r") as api_key_file:
        api_key_values = json.loads(api_key_file.read())

    openai.organization = api_key_values["openai"]["organization"]
    openai.api_key = api_key_values["openai"]["api_key"]

    # Neues Bild erzeugen und anzeigen
    print("Erzeuge neues Bild")

    response = openai.Image.create(prompt="Astronaut with cowboy hat riding horse on Mars", n=1, size="512x512")
    image_url = response['data'][0]['url']

    webbrowser.open(image_url)
