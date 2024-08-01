from googletrans import Translator

def translate(text, dest_language):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language.lower())
    return translated.text
