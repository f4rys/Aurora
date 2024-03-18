from modules.dictionaries.dictionaries import dictionary_en, dictionary_pl

from configparser import ConfigParser

def load_dictionary():
    languages = {"en" : dictionary_en, "pl": dictionary_pl}
    config = ConfigParser()
    config.read('settings.ini')
    dictionary = languages[config['GUI']['interface_language']]

    return dictionary