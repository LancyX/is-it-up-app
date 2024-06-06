"""Pack of translations, used by app"""
import json

async def read_translation(language: str):
    """return translation data for desired language"""
    with open('../translations/translations.json', 'r', encoding="utf=8") as file:
        data = json.loads(file.read())
        return data[language]

async def read_titles():
    """return translation data for desired language"""
    with open('../translations/titles.json', 'r', encoding="utf=8") as file:
        data = json.loads(file.read())
        return data
