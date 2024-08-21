import unittest
from configparser import ConfigParser
from modules.dictionaries import dictionary_en, dictionary_pl, load_dictionary


class LoadDictionaryTest(unittest.TestCase):
    DEFAULT_SETTINGS = """
        [GUI]
        interface_language = en

        [General]
        smart_mode = off
        max_retry = 3
    """

    def setUp(self):
        self.config_file_path = "settings.ini"
        config = ConfigParser()
        config.add_section('GUI')
        config.set('GUI', 'interface_language', 'en')
        with open(self.config_file_path, 'w', encoding="utf-8") as configfile:
            config.write(configfile)

    def tearDown(self):
        with open("settings.ini", "w", encoding="utf-8") as f:
            f.write(self.DEFAULT_SETTINGS)

    def test_load_english_dictionary(self):
        """
        Verifies that `load_dictionary` returns the English dictionary when the
        interface language is set to 'en' in the configuration file.
        """

        result = load_dictionary()
        self.assertEqual(result, dictionary_en)

    def test_load_polish_dictionary(self):
        """
        Verifies that `load_dictionary` returns the Polish dictionary when the
        interface language is set to 'pl' in the configuration file.
        """

        config = ConfigParser()
        config.read(self.config_file_path)
        config.set('GUI', 'interface_language', 'pl')
        with open(self.config_file_path, 'w', encoding="utf-8") as configfile:
            config.write(configfile)

        result = load_dictionary()
        self.assertEqual(result, dictionary_pl)

    def test_invalid_language_raises_error(self):
        """
        Verifies that `load_dictionary` raises a `KeyError` when the interface language
        in the configuration file is set to an invalid value.
        """

        config = ConfigParser()
        config.read(self.config_file_path)
        config.set('GUI', 'interface_language', 'invalid')
        with open(self.config_file_path, 'w', encoding="utf-8") as configfile:
            config.write(configfile)

        with self.assertRaises(KeyError):
            load_dictionary()