"""
Konkrete Implementierung eines Text2Image-Generators für OpenAPI DALL-E.
Ruft den OpenAPI-Webservice auf, um ein Bild zu generieren.
"""

from ipaint.generator.base import Text2Image, GeneratedImage
import openai

class Text2Image_OpenAI_DallE(Text2Image):
    """
    Implementierung der Text2Image-Basisklasse für OpenAI DALL-E.
    """
    def generate(self, prompt):
        """
        Methode zum Aufrufen der Bildgenerierung.
        """
        openai.organization = self._api_key["organization"]
        openai.api_key = self._api_key["api_key"]

        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        image_url = response['data'][0]['url']

        return GeneratedImage(prompt, image_url, "png")