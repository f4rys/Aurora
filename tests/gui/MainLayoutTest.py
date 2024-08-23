import unittest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QFrame
from modules.gui import MainLayout


class MainLayoutTest(unittest.TestCase):
    def setUp(self):
        self.main_layout = MagicMock(spec=MainLayout)

        mock_frame = MagicMock(spec=QFrame)
        mock_frame.frameShape.return_value = QFrame.Shape.HLine
        mock_frame.frameShadow.return_value = QFrame.Shadow.Sunken

        self.main_layout.line = mock_frame

    def test_initialization(self):
        """Test that MainLayout initializes correctly with a line QFrame."""
        self.assertIsInstance(self.main_layout.line, QFrame)
        self.assertEqual(self.main_layout.line.frameShape(), QFrame.Shape.HLine)
        self.assertEqual(self.main_layout.line.frameShadow(), QFrame.Shadow.Sunken)


if __name__ == '__main__':
    unittest.main()
