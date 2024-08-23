import unittest
from PyQt6.QtWidgets import QApplication, QSizePolicy

from modules.dictionaries.loader import load_dictionary
from modules.gui.device import BulbSwitchButton


class BulbSwitchButtonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.button = BulbSwitchButton()

    def test_initial_tooltip(self):
        """Test that the initial tooltip is set correctly."""
        dictionary = load_dictionary()
        self.assertEqual(self.button.toolTip(), dictionary["bulb_tooltip"])

    def test_set_icon_on(self):
        """Test setting the icon to 'on' state."""
        self.button.set_icon(True)
        self.assertIn("bulb_on.png", self.button.styleSheet())

    def test_set_icon_off(self):
        """Test setting the icon to 'off' state."""
        self.button.set_icon(False)
        self.assertIn("bulb_off.png", self.button.styleSheet())

    def test_size_policy(self):
        """Test that the size policy is set correctly."""
        size_policy = self.button.sizePolicy()
        self.assertEqual(size_policy.horizontalPolicy(), QSizePolicy.Policy.Expanding)
        self.assertEqual(size_policy.verticalPolicy(), QSizePolicy.Policy.Expanding)

    def test_set_property_class(self):
        """Test that the 'class' property is set correctly."""
        self.assertEqual(self.button.property("class"), "switch")

    def test_dictionary_loading(self):
        """Test that the dictionary is loaded correctly."""
        self.assertIsNotNone(self.button.dictionary)
        self.assertIsInstance(self.button.dictionary, dict)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
