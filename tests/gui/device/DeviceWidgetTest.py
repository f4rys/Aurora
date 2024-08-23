import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication

from modules.gui.device import DeviceWidget, BulbSwitchButton
from modules.gui.device.tabs import WhiteModeTab, ColourModeTab, CountdownTab


class DeviceWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.widget = DeviceWidget()

        self.mock_device = MagicMock()
        self.mock_device.read_current_countdown.return_value = 10
        self.mock_device.is_rgb = True
        self.mock_device.is_on.return_value = True
        self.mock_device.hsv_range = {"h": (0, 360), "s": (0, 100), "v": (0, 100)}
        self.mock_device.brightness_range = (0, 100)
        self.mock_device.temperature_range = (2700, 6500)
        self.mock_device.get_mode.return_value = "white"
        self.mock_device.get_hsv.return_value = 1, 2, 3

        self.mock_dictionary = {
            "white": "White Mode",
            "colour": "Colour Mode",
            "countdown": "Countdown"
        }

        patcher = patch('modules.dictionaries.loader.load_dictionary', return_value=self.mock_dictionary)
        self.addCleanup(patcher.stop)
        self.mock_load_dictionary = patcher.start()

        patcher_clear_layout = patch('modules.gui.tools.clear_layout')
        self.addCleanup(patcher_clear_layout.stop)
        self.mock_clear_layout = patcher_clear_layout.start()

        self.widget.white_tab = MagicMock(spec=WhiteModeTab)
        self.widget.colour_tab = MagicMock(spec=ColourModeTab)
        self.widget.countdown_tab = MagicMock(spec=CountdownTab)

        self.widget.bulb_button = MagicMock(spec=BulbSwitchButton)
        self.widget.bulb_button.set_icon = MagicMock()

        self.widget.init_ui(self.mock_device)

    def test_switch_on_to_off(self):
        """Test switching the device from 'on' to 'off'."""
        with patch.object(BulbSwitchButton, 'set_icon', new_callable=MagicMock) as mock_set_icon:
            self.mock_device.is_on.return_value = True
            self.widget.init_ui(self.mock_device)
            self.widget.switch()

            self.mock_device.turn_off.assert_called_once()
            mock_set_icon.assert_called()

    def test_switch_off_to_on(self):
        """Test switching the device from 'off' to 'on'."""
        with patch.object(BulbSwitchButton, 'set_icon', new_callable=MagicMock) as mock_set_icon:
            self.mock_device.is_on.return_value = False
            self.widget.init_ui(self.mock_device)
            self.widget.switch()

            self.mock_device.turn_on.assert_called_once()
            mock_set_icon.assert_called()

    def test_set_brightness(self):
        """Test setting the device's brightness."""
        self.widget.init_ui(self.mock_device)

        self.widget.tab_widget.setCurrentIndex(0)
        self.widget.white_tab.brightness_slider.setValue(75)

        self.widget.set_brightness()
        self.mock_device.device.set_brightness.assert_called_with(75)

    def test_set_temperature(self):
        """Test setting the device's color temperature."""
        self.widget.init_ui(self.mock_device)
        self.widget.white_tab.temperature_slider.setValue(3000)
        self.widget.set_temperature()

        self.mock_device.device.set_colourtemp.assert_called_with(3000)

    def test_set_hsv(self):
        """Test setting the device's HSV values."""
        self.widget.init_ui(self.mock_device)

        self.widget.colour_tab.hue_slider.setValue(120)
        self.widget.colour_tab.saturation_slider.setValue(80)
        self.widget.colour_tab.value_slider.setValue(90)

        self.widget.set_hsv()
        self.mock_device.set_hsv.assert_called_with(120, 80, 90)

    def test_init_ui_rgb_device(self):
        """Test UI initialization for an RGB device."""
        self.mock_device.is_rgb = True
        self.widget.init_ui(self.mock_device)
        self.assertEqual(self.widget.tab_widget.count(), 3)
        self.assertTrue(isinstance(self.widget.colour_tab, ColourModeTab))

    def test_init_ui_non_rgb_device(self):
        """Test UI initialization for a non-RGB device."""
        self.mock_device.is_rgb = False
        self.widget.init_ui(self.mock_device)
        self.assertEqual(self.widget.tab_widget.count(), 2)

    def test_set_initial_tab(self):
        """Test setting the initial tab based on the device mode."""
        self.widget.init_ui(self.mock_device)

        self.mock_device.get_mode.return_value = "white"
        self.widget.set_initial_tab()
        self.assertEqual(self.widget.tab_widget.currentIndex(), 0)

        self.mock_device.get_mode.return_value = "colour"
        self.widget.set_initial_tab()
        self.assertEqual(self.widget.tab_widget.currentIndex(), 1)

    @classmethod
    def tearDownClass(cls):
        cls.app.exit()
        del cls.app


if __name__ == '__main__':
    unittest.main()
