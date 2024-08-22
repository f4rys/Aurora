import unittest
from PyQt6.QtWidgets import QApplication

from modules.gui.help import HelpWidget


class HelpWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.widget = HelpWidget()

    def test_initialization(self):
        """Test if the HelpWidget initializes correctly."""
        self.assertIsInstance(self.widget, HelpWidget)
        self.assertIsNotNone(self.widget.scroll_area)
        self.assertIsNotNone(self.widget.scroll_widget)

    def test_dictionary_loading(self):
        """Test if the dictionary is loaded correctly."""
        self.assertIsNotNone(self.widget.dictionary)
        self.assertIn("tooltips_q", self.widget.dictionary)
        self.assertIn("tooltips_a", self.widget.dictionary)

    def test_faq_label_exists(self):
        """Test if the FAQ label is created."""
        self.assertEqual(self.widget.faq_label.text(), "FAQ")

    def test_tooltips_question_label(self):
        """Test if the tooltips question label is created correctly."""
        self.assertEqual(self.widget.tooltips_q_label.text(), self.widget.dictionary["tooltips_q"])

    def test_email_link(self):
        """Test if the email link is set correctly."""
        expected_email = "wojciech.michal.bartoszek@gmail.com"
        self.assertIn(expected_email, self.widget.email_label.text())

    def test_repository_link(self):
        """Test if the repository link is set correctly."""
        expected_repo = "https://github.com/f4rys/Aurora"
        self.assertIn(expected_repo, self.widget.repository_label.text())

    def test_invalid_dictionary_key(self):
        """Test if accessing an invalid key in the dictionary raises KeyError."""
        with self.assertRaises(KeyError):
            _ = self.widget.dictionary["invalid_key"]

    def test_widget_properties(self):
        """Test if widget properties are set correctly."""
        self.assertEqual(self.widget.scroll_area.property("class"), "borderless")
        self.assertEqual(self.widget.scroll_widget.property("class"), "borderless")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == '__main__':
    unittest.main()
