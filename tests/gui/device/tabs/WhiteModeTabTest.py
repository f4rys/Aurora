import unittest

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from modules.gui.device.tabs import WhiteModeTab
from modules.dictionaries.loader import load_dictionary


class WhiteModeTabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.white_mode_tab = WhiteModeTab()

    def test_brightness_slider_properties(self):
        """Test the properties of the brightness slider."""
        slider = self.white_mode_tab.brightness_slider
        self.assertEqual(slider.orientation(), Qt.Orientation.Horizontal)
        self.assertEqual(slider.tickPosition(), slider.TickPosition.TicksBelow)
        self.assertEqual(slider.property("class"), "brightness_slider")
        self.assertEqual(slider.toolTip(), load_dictionary()["brightness_tooltip"])

    def test_temperature_slider_properties(self):
        """Test the properties of the temperature slider."""
        slider = self.white_mode_tab.temperature_slider
        self.assertEqual(slider.orientation(), Qt.Orientation.Horizontal)
        self.assertEqual(slider.tickPosition(), slider.TickPosition.TicksBelow)
        self.assertEqual(slider.property("class"), "warmth_slider")
        self.assertEqual(slider.toolTip(), load_dictionary()["temperature_tooltip"])

    def test_layout_contains_widgets(self):
        """Test if the layout contains the correct widgets."""
        layout = self.white_mode_tab.vlayout
        self.assertEqual(layout.count(), 2)
        self.assertEqual(layout.itemAt(0).widget(), self.white_mode_tab.brightness_slider)
        self.assertEqual(layout.itemAt(1).widget(), self.white_mode_tab.temperature_slider)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
