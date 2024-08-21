import unittest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication
from modules.gui.all_devices import AllDevicesWidget

class AllDevicesWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.parent_mock = MagicMock()
        self.widget = AllDevicesWidget(self.parent_mock)

    def test_open_device(self):
        """Tests the open_device method of the AllDevicesWidget class."""
        device_mock = MagicMock()
        self.widget.open_device(device_mock)
        self.parent_mock.parent.parent.show_device.assert_called_with(device_mock)

    def test_add_reload_button(self):
        """Tests the add_reload_button method of the AllDevicesWidget class."""
        text = "Reload"
        self.widget.add_reload_button(text)
        self.assertEqual(self.widget.reload_button.text(), text)
        self.assertTrue(self.widget.reload_button.isEnabled())

    def test_switch_device_on(self):
        """Tests the switch method of the AllDevicesWidget class when switching a device on."""
        device_mock = MagicMock()
        device_mock.is_on.return_value = False
        device_status_button = MagicMock()
        device_button = MagicMock()
        self.widget.switch(device_mock, True, device_status_button, device_button)
        device_mock.turn_on.assert_called_once()
        device_status_button.clicked.connect.assert_called_once()

    def test_switch_device_off(self):
        """Tests the switch method of the AllDevicesWidget class when switching a device off."""
        device_mock = MagicMock()
        device_mock.is_on.return_value = True
        device_status_button = MagicMock()
        device_button = MagicMock()
        self.widget.switch(device_mock, False, device_status_button, device_button)
        device_mock.turn_off.assert_called_once()
        device_status_button.clicked.connect.assert_called_once()

    def test_set_icon_and_action_device_on(self):
        """Tests the set_icon_and_action method of the AllDevicesWidget class when the device is on."""
        device_mock = MagicMock()
        device_mock.is_on.return_value = True
        device_status_button = MagicMock()
        device_button = MagicMock()
        self.widget.set_icon_and_action(device_status_button, device_button, device_mock)
        device_status_button.setIcon.assert_called_once()
        device_status_button.setToolTip.assert_called_once()

    def test_set_icon_and_action_device_off(self):
        """Tests the set_icon_and_action method of the AllDevicesWidget class when the device is off."""
        device_mock = MagicMock()
        device_mock.is_on.return_value = False
        device_status_button = MagicMock()
        device_button = MagicMock()
        self.widget.set_icon_and_action(device_status_button, device_button, device_mock)
        device_status_button.setIcon.assert_called_once()
        device_status_button.setToolTip.assert_called_once()

    def test_add_device_button(self):
        """Tests the add_device_button method of the AllDevicesWidget class."""
        name = "Device1"
        icon_link = "http://example.com/icon.png"
        device_mock = MagicMock()
        layout = self.widget.add_device_button(name, icon_link, device_mock)
        self.assertEqual(layout.count(), 3)

    def tearDown(self):
        if hasattr(self, 'widget') and self.widget.thread_worker.isRunning():
            self.widget.thread_worker.quit()
            self.widget.thread_worker.wait()
        self.widget.deleteLater()
        self.parent_mock = None

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
