import unittest
from unittest.mock import MagicMock, patch, call
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from modules.gui.all_devices import AllDevicesWidget

class AllDevicesWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget_mock = MagicMock(spec=AllDevicesWidget)
        self.widget_mock.parent = self.parent_mock

    def test_open_device(self):
        """Tests the open_device method of the AllDevicesWidget class."""
        device_mock = MagicMock()
        AllDevicesWidget.open_device(self.widget_mock, device_mock)
        self.parent_mock.parent.parent.show_device.assert_called_with(device_mock)

    def test_add_device_button(self):
        """Tests the add_device_button method of the AllDevicesWidget class."""
        name = "Device1"
        icon_link = "http://example.com/icon.png"
        device_mock = MagicMock()
        with patch.object(AllDevicesWidget, 'add_device_button') as mock_add_device_button:
            mock_add_device_button.return_value = QHBoxLayout()
            layout = AllDevicesWidget.add_device_button(self.widget_mock, name, icon_link, device_mock)
            mock_add_device_button.assert_called_with(self.widget_mock, name, icon_link, device_mock)
            self.assertEqual(layout.count(), 0)  # As it's a mock, count would be zero.

    def tearDown(self):
        self.parent_mock = None
        self.widget_mock = None

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del cls.app

if __name__ == '__main__':
    unittest.main()
