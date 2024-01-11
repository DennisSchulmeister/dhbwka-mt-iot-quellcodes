import json, os, webbrowser
import rich

from openai import OpenAI
from rich.prompt import Prompt

## Die folgenden Zeilen einkommentieren, um den Ablauf auf der Konsole zu tracen
# import snoop
# @snoop
def main():
    """
    Funktion mit der eigentlichen Programmlogik.
    """
    ## Die folgende Zeile einkommentieren, um das Programm in der Konsole zu debuggen
    # import pudb; pu.db

    # API-Key einlesen und OpenAI-Client erzeugen
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "..", "API_KEY.json")

    with open(file_path, "r") as api_key_file:
        api_key_values = json.loads(api_key_file.read())

    openai_client = OpenAI(
        organization = api_key_values["openai"]["organization"],
        api_key      = api_key_values["openai"]["api_key"],
    )

    # Benutzer nach dem Prompt fragen
    prompt = Prompt.ask(
        "[bold bright_magenta]Welches Bild soll generiert werden?[/bold bright_magenta]",
        #default="Astronaut with cowboy hat riding horse on Mars"
    )

    # Wenn nichts eingegeben wurde, soll ChatGPT sich einen Prompt ausdenken
    if not prompt:
        chat_response = openai_client.chat.completions.create(
           model    = "gpt-3.5-turbo",
           messages = [{
              "role": "user",
              "content": "Please suggest a prompt to generate an image with DALL-E. Reply with the prompt only."
           }],
        )

        prompt = chat_response.choices[0].message.content
        rich.inspect(prompt)

    # Neues Bild erzeugen und anzeigen
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
