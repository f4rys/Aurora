import unittest
from PyQt6.QtWidgets import QApplication, QSlider
from PyQt6.QtCore import Qt

from modules.gui.device.tabs import ColourModeTab


class ColourModeTabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.tab = ColourModeTab()

    def test_hue_slider_initialization(self):
        """Test the initialization and properties of the hue slider."""
        self.assertIsInstance(self.tab.hue_slider, QSlider)
        self.assertEqual(self.tab.hue_slider.orientation(), Qt.Orientation.Horizontal)
        self.assertEqual(self.tab.hue_slider.property("class"), "colour_slider")
        self.assertIn("colour_tooltip", self.tab.dictionary)

    def test_saturation_slider_initialization(self):
        """Test the initialization and properties of the saturation slider."""
        self.assertIsInstance(self.tab.saturation_slider, QSlider)
        self.assertEqual(self.tab.saturation_slider.orientation(), Qt.Orientation.Horizontal)
        self.assertEqual(self.tab.saturation_slider.property("class"), "contrast_slider")
        self.assertIn("contrast_tooltip", self.tab.dictionary)

    def test_value_slider_initialization(self):
        """Test the initialization and properties of the value slider."""
        self.assertIsInstance(self.tab.value_slider, QSlider)
        self.assertEqual(self.tab.value_slider.orientation(), Qt.Orientation.Horizontal)
        self.assertEqual(self.tab.value_slider.property("class"), "brightness_slider")
        self.assertIn("brightness_tooltip", self.tab.dictionary)

    def test_tooltips(self):
        """Test that the sliders' tooltips match the expected values from the dictionary."""
        self.assertEqual(self.tab.hue_slider.toolTip(), self.tab.dictionary["colour_tooltip"])
        self.assertEqual(self.tab.saturation_slider.toolTip(), self.tab.dictionary["contrast_tooltip"])
        self.assertEqual(self.tab.value_slider.toolTip(), self.tab.dictionary["brightness_tooltip"])

    def test_invalid_slider_class(self):
        """Test that an invalid slider class does not match any expected classes."""
        invalid_slider = QSlider()
        invalid_slider.setProperty("class", "invalid_slider")
        self.assertNotEqual(invalid_slider.property("class"), "colour_slider")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == "__main__":
    unittest.main()
