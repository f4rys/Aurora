import unittest
from PyQt6.QtWidgets import QApplication, QSizePolicy
from PyQt6.QtCore import Qt

from modules.dictionaries.loader import load_dictionary
from modules.gui.device import BulbNameLabel


class BulbNameLabelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.label = BulbNameLabel("Test Bulb")

    def test_initialization_with_valid_name(self):
        """Test initialization with a valid name."""
        self.assertEqual(self.label.text(), "Test Bulb")
        self.assertEqual(self.label.toolTip(), load_dictionary()["bulb_label_tooltip"])

    def test_set_text(self):
        """Test set_text method with valid input."""
        self.label.set_text("New Bulb")
        self.assertEqual(self.label.text(), "New Bulb")

    def test_set_text_empty(self):
        """Test set_text method with empty string."""
        self.label.set_text("")
        self.assertEqual(self.label.text(), "")

    def test_size_policy(self):
        """Test if size policy is set correctly."""
        size_policy = self.label.sizePolicy()
        self.assertEqual(size_policy.horizontalPolicy(), QSizePolicy.Policy.Expanding)
        self.assertEqual(size_policy.verticalPolicy(), QSizePolicy.Policy.Fixed)

    def test_alignment(self):
        """Test if alignment is set correctly."""
        self.assertEqual(self.label.alignment(), Qt.AlignmentFlag.AlignCenter)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
