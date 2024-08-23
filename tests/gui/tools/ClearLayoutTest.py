import unittest
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

from modules.gui.tools import clear_layout


class ClearLayoutTest(unittest.TestCase):
    """Test suite for the `clear_layout` function from the `modules.gui.tools` module."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a QApplication instance before running any tests.

        This is necessary for creating and managing Qt widgets within the tests.
        """

        cls.app = QApplication([])

    def test_clear_layout_with_widgets(self):
        """
        Verifies that `clear_layout` removes all widgets from a QVBoxLayout containing widgets.

        This test creates a QWidget with a QVBoxLayout, adds a QLabel and a QPushButton to the layout,
        verifies the initial widget count, and then calls `clear_layout`. Finally, it checks that the
        widget count is zero after clearing the layout.
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        label = QLabel("Test Label")
        button = QPushButton("Test Button")
        layout.addWidget(label)
        layout.addWidget(button)

        self.assertEqual(layout.count(), 2, "Layout should initially contain two widgets")

        clear_layout(layout)

        self.assertEqual(layout.count(), 0, "Layout should be empty after clearing")

    def test_clear_layout_with_nested_layouts(self):
        """
        Verifies that `clear_layout` removes all widgets from a QVBoxLayout containing a nested layout.

        This test creates a QWidget with a main QVBoxLayout, adds a nested QVBoxLayout,
        adds a QLabel and a QPushButton to the nested layout, verifies the initial widget counts
        for both layouts, then calls `clear_layout` on the main layout. Finally, it checks that
        both the main and nested layouts are empty after clearing.
        """

        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        nested_layout = QVBoxLayout()
        label = QLabel("Nested Label")
        button = QPushButton("Nested Button")
        nested_layout.addWidget(label)
        nested_layout.addWidget(button)

        main_layout.addLayout(nested_layout)

        self.assertEqual(main_layout.count(), 1, "Main layout should initially contain one nested layout")
        self.assertEqual(nested_layout.count(), 2, "Nested layout should initially contain two widgets")

        clear_layout(main_layout)

        self.assertEqual(main_layout.count(), 0, "Main layout should be empty after clearing")

    @classmethod
    def tearDownClass(cls):
        """
        Quits the QApplication instance after all tests are finished.

        This ensures that Qt resources are properly released when the tests are complete.
        """

        cls.app.quit()
        del cls.app

if __name__ == '__main__':
    unittest.main()