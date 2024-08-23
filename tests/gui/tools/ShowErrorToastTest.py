import unittest
from unittest.mock import patch
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QApplication
from pyqttoast import ToastPreset

from modules.gui.tools import show_error_toast


class ShowErrorToastTest(unittest.TestCase):
    """Test suite for the `show_error_toast` function."""

    @classmethod
    def setUpClass(cls):
        """
        Creates a QApplication instance before running any tests.

        This is necessary for creating and managing Qt widgets within the tests.
        """

        cls.app = QApplication([])

    @patch('modules.gui.tools.show_error_toast.load_dictionary')
    @patch('modules.gui.tools.show_error_toast.Toast')
    def test_show_error_toast(self, MockToast, mock_load_dictionary):
        """
        Verifies the behavior of `show_error_toast` using mocks.

        This test uses `unittest.mock.patch` to mock the `load_dictionary` and `Toast` functions.
        It sets up the mock `load_dictionary` to return a dictionary containing the expected error toast
        text and title. It then calls `show_error_toast` with a parent widget and verifies the following:

        - `load_dictionary` is called once to retrieve the error toast text and title.
        - `Toast` is called once with the parent widget as an argument.
        - The mock `Toast` instance's methods are called with the expected configuration for an error toast:
            - `setAlwaysOnMainScreen` with `True`
            - `setShowDurationBar` with `False`
            - `setBorderRadius` with `15`
            - `setResetDurationOnHover` with `False`
            - `setMaximumWidth` with `300`
            - `setMaximumHeight` with `100`
            - `setDuration` with `5000` (milliseconds)
            - `setBackgroundColor` with a specific color code
            - `setTitle` with the error toast title
            - `setText` with the error toast body text
            - `applyPreset` with `ToastPreset.ERROR`
            - `show` to display the toast
        """

        mock_load_dictionary.return_value = {
            "error_toast_title": "Error",
            "error_toast_body": "An error occurred."
        }

        parent = QWidget()
        show_error_toast(parent)

        mock_load_dictionary.assert_called_once()
        MockToast.assert_called_once_with(parent)

        mock_toast_instance = MockToast.return_value

        mock_toast_instance.setAlwaysOnMainScreen.assert_called_once_with(True)
        mock_toast_instance.setShowDurationBar.assert_called_once_with(False)
        mock_toast_instance.setBorderRadius.assert_called_once_with(15)
        mock_toast_instance.setResetDurationOnHover.assert_called_once_with(False)
        mock_toast_instance.setMaximumWidth.assert_called_once_with(300)
        mock_toast_instance.setMaximumHeight.assert_called_once_with(100)
        mock_toast_instance.setDuration.assert_called_once_with(5000)
        mock_toast_instance.setBackgroundColor.assert_called_once_with(QColor('#DAD9D3'))
        mock_toast_instance.setTitle.assert_called_once_with("Error")
        mock_toast_instance.setText.assert_called_once_with("An error occurred.")
        mock_toast_instance.applyPreset.assert_called_once_with(ToastPreset.ERROR)
        mock_toast_instance.show.assert_called_once()

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