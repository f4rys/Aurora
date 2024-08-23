import unittest

from PyQt6.QtWidgets import QApplication

from modules.gui import ActionBarLayout


class ActionBarLayoutTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.layout = ActionBarLayout()

    def test_initialization(self):
        """Test the initial state of ActionBarLayout."""
        self.assertIsInstance(self.layout, ActionBarLayout)
        self.assertEqual(self.layout.label.text(), "")
        self.assertEqual(self.layout.button_group.count(), 4)

    def test_set_label(self):
        """Test setting the label text."""
        test_text = "Profile"
        self.layout.set_label(test_text)
        self.assertEqual(self.layout.label.text(), test_text)

    def test_tooltips(self):
        """Test tooltips for buttons."""
        self.assertEqual(self.layout.profile_button.toolTip(), self.layout.dictionary["profile_tooltip"])
        self.assertEqual(self.layout.settings_button.toolTip(), self.layout.dictionary["settings_tooltip"])
        self.assertEqual(self.layout.hide_button.toolTip(), self.layout.dictionary["hide_tooltip"])
        self.assertEqual(self.layout.exit_button.toolTip(), self.layout.dictionary["exit_tooltip"])

    def test_button_properties(self):
        """Test button properties."""
        self.assertEqual(self.layout.profile_button.objectName(), "profile_button")
        self.assertEqual(self.layout.settings_button.objectName(), "settings_button")
        self.assertEqual(self.layout.hide_button.objectName(), "hide_button")
        self.assertEqual(self.layout.exit_button.objectName(), "exit_button")

    def test_button_count(self):
        """Test the count of buttons in the button group."""
        self.assertEqual(self.layout.button_group.count(), 4)

    def tearDown(self):
        self.app.quit()
        del self.app
        del self.layout


if __name__ == "__main__":
    unittest.main()
