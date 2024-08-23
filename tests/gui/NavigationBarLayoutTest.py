import unittest
from PyQt6.QtWidgets import QApplication, QToolButton
from modules.gui import NavigationBarLayout


class NavigationBarLayoutTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.layout = NavigationBarLayout()

    def test_initialization(self):
        """Test that NavigationBarLayout initializes correctly."""
        self.assertIsInstance(self.layout, NavigationBarLayout)
        self.assertEqual(self.layout.count(), 9)

    def test_button_count(self):
        """Test that NavigationBarLayout contains the correct number of QToolButtons."""
        button_count = sum(1 for i in range(self.layout.count()) if isinstance(self.layout.itemAt(i).widget(), QToolButton))
        self.assertEqual(button_count, 5)

    def test_dictionary_loading(self):
        """Test that the navigation dictionary is loaded correctly."""
        self.assertIsNotNone(self.layout.dictionary)
        self.assertIn("devices", self.layout.dictionary)
        self.assertIn("schedules", self.layout.dictionary)
        self.assertIn("analytics", self.layout.dictionary)
        self.assertIn("smart_mode", self.layout.dictionary)
        self.assertIn("help", self.layout.dictionary)

    def test_button_properties(self):
        """Test that the devices button has the correct properties."""
        devices_button = self.layout.devices_button
        self.assertTrue(devices_button.isCheckable())
        self.assertIn(devices_button.icon().name(), ":/navigation/devices.png")
        self.assertEqual(devices_button.text(), self.layout.dictionary["devices"])

    def test_button_group_exclusivity(self):
        """Test that the button group ensures only one button is checked at a time."""
        self.layout.devices_button.setChecked(True)
        self.layout.schedules_button.setChecked(True)
        self.assertFalse(self.layout.devices_button.isChecked())

    def tearDown(self):
        self.app.exit()
        del self.app
        del self.layout


if __name__ == '__main__':
    unittest.main()
