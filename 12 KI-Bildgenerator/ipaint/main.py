#! /usr/bin/env python3

import json, os, webbrowser
import rich

from openai import OpenAI
from rich.prompt import Prompt

#import pysnooper

#@pysnooper.snoop()
def main():
    """
    Funktion mit der eigentlichen Programmlogik.
    """
    # API-Key einlesen
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "..", "API_KEY.json")

    with open(file_path, "r") as api_key_file:
        api_key_values = json.loads(api_key_file.read())

    openai_client = OpenAI(
        organization = api_key_values["openai"]["organization"],
        api_key      = api_key_values["openai"]["api_key"],
    )

    # Neues Bild erzeugen und anzeigen
    prompt = Prompt.ask(
        "[bold bright_magenta]Welches Bild soll generiert werden?[/bold bright_magenta]",
        default="Astronaut with cowboy hat riding horse on Mars"
    )

    response = openai_client.images.generate(
        model   = "dall-e-3",
        prompt  = prompt,
        size    = "1024x1024",
        quality = "standard",
        n       = 1,
    )

    rich.inspect(response, methods=False)

    image_url = response.data[0].url
    webbrowser.open(image_url)
