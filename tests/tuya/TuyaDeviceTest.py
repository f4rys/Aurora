import unittest
from unittest.mock import patch, MagicMock

from modules.tuya import TuyaDevice


class TuyaDeviceTest(unittest.TestCase):
    def setUp(self):
        """Set up test environment and mock device."""
        self.dev_id = 'test_id'
        self.local_key = 'test_key'
        self.ip = '192.168.1.100'
        self.version = '3.3'
        self.name = 'Test Bulb'
        self.icon_link = 'http://example.com/icon.png'
        self.brightness_range = [1, 100]
        self.temperature_range = [2700, 6500]
        self.is_rgb = True
        self.hsv_range = {'h': [0, 360], 's': [0, 100], 'v': [0, 100]}
        self.has_countdown = True
        self.countdown_range = [1, 3600]

        self.mock_bulb_device = MagicMock()
        self.mock_bulb_device.id = self.dev_id

        with patch('tinytuya.BulbDevice') as mock_bulb_device_constructor:
            mock_bulb_device_constructor.return_value = self.mock_bulb_device
            self.device = TuyaDevice(self.dev_id, self.local_key, self.ip, self.version, 
                                     self.name, self.icon_link, self.brightness_range, 
                                     self.temperature_range, self.is_rgb, self.hsv_range, 
                                     self.has_countdown, self.countdown_range)

    def test_init(self):
        """Test initialization of TuyaDevice."""
        self.assertEqual(self.device.id, self.dev_id)
        self.assertEqual(self.device.local_key, self.local_key)
        self.assertEqual(self.device.version, self.version)

    def test_turn_on_off(self):
        """Test turning device on and off."""
        self.device.turn_on()
        self.mock_bulb_device.turn_on.assert_called_once()

        self.device.turn_off()
        self.mock_bulb_device.turn_off.assert_called_once()

    def test_is_on(self):
        """Test checking if device is on."""
        self.mock_bulb_device.state.return_value = {'is_on': True}
        self.assertTrue(self.device.is_on())

        self.mock_bulb_device.state.return_value = {'is_on': False}
        self.assertFalse(self.device.is_on())

        self.mock_bulb_device.state.side_effect = Exception('Test exception')
        self.assertFalse(self.device.is_on())

    def test_get_brightness_temperature(self):
        """Test getting brightness and temperature values."""
        self.mock_bulb_device.brightness.return_value = 50
        self.assertEqual(self.device.get_brightness(), 50)

        self.mock_bulb_device.colourtemp.return_value = 4000
        self.assertEqual(self.device.get_temperature(), 4000)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"test_id": 1692214664.0}')
    @patch('time.time') 
    def test_read_current_countdown_existing(self, mock_time, mock_open, mock_exists):
        """Test reading current countdown with existing file."""
        mock_exists.return_value = True
        mock_time.return_value = 1692214000.0 
        self.assertEqual(self.device.read_current_countdown(), 1692214664.0)

        mock_time.return_value = 1692215000.0 
        self.assertEqual(self.device.read_current_countdown(), 0) 

    def test_set_mode_get_mode(self):
        """Test setting and getting mode."""
        self.device.set_mode(1)
        self.mock_bulb_device.set_mode.assert_called_with('colour')

        self.device.set_mode(0)
        self.mock_bulb_device.set_mode.assert_called_with('white')

        self.mock_bulb_device.state.return_value = {'mode': 'colour'}
        self.assertEqual(self.device.get_mode(), 'colour')

    def test_set_hsv_get_hsv(self):
        """Test setting and getting HSV values."""
        self.device.set_hsv(180, 50, 80)
        self.mock_bulb_device.set_hsv.assert_called_with(0.5, 0.5, 0.8)

        self.mock_bulb_device.colour_hsv.return_value = (0.25, 0.75, 0.6)
        self.assertEqual(self.device.get_hsv(), (0.25, 0.75, 0.6))


if __name__ == '__main__':
    unittest.main()
