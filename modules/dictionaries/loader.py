from configparser import ConfigParser

from modules.dictionaries import dictionary_en, dictionary_pl

def load_dictionary():
    languages = {"en" : dictionary_en, "pl": dictionary_pl}
    config = ConfigParser()
    config.read('settings.ini')
    dictionary = languages[config['GUI']['interface_language']]

    return dictionary