from time import sleep
from googletrans import Translator


def translate(text):
    translator = Translator()
    translation = translator.translate(text=text, src="it", dest="ru").text
    return translation
