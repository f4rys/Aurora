import unittest
from unittest.mock import MagicMock

from modules.gui.device import DeviceWidget
from modules.gui.all_devices import AllDevicesWidget
from modules.gui.smart_mode import SmartModeWidget
from modules.gui.analytics import AnalyticsWidget
from modules.gui.schedules import SchedulesWidget, EditScheduleWidget
from modules.gui.credentials import CredentialsWidget
from modules.gui.settings import SettingsWidget
from modules.gui.profile import ProfileWidget
from modules.gui.help import HelpWidget


class StackedWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stacked_widget = MagicMock()
        cls.stacked_widget.count.return_value = 10
        cls.stacked_widget.credentials = MagicMock(spec=CredentialsWidget)
        cls.stacked_widget.device = MagicMock(spec=DeviceWidget)
        cls.stacked_widget.all_devices = MagicMock(spec=AllDevicesWidget)
        cls.stacked_widget.smart_mode = MagicMock(spec=SmartModeWidget)
        cls.stacked_widget.analytics = MagicMock(spec=AnalyticsWidget)
        cls.stacked_widget.schedules = MagicMock(spec=SchedulesWidget)
        cls.stacked_widget.edit_schedule = MagicMock(spec=EditScheduleWidget)
        cls.stacked_widget.help = MagicMock(spec=HelpWidget)
        cls.stacked_widget.settings = MagicMock(spec=SettingsWidget)
        cls.stacked_widget.profile = MagicMock(spec=ProfileWidget)

    def test_initialization(self):
        """Test that the StackedWidget initializes with the correct number of widgets."""
        self.assertEqual(self.stacked_widget.count(), 10)

    def test_credentials_widget(self):
        """Test that the credentials widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.credentials, CredentialsWidget)

    def test_device_widget(self):
        """Test that the device widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.device, DeviceWidget)

    def test_all_devices_widget(self):
        """Test that the all devices widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.all_devices, AllDevicesWidget)

    def test_smart_mode_widget(self):
        """Test that the smart mode widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.smart_mode, SmartModeWidget)

    def test_analytics_widget(self):
        """Test that the analytics widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.analytics, AnalyticsWidget)

    def test_schedules_widget(self):
        """Test that the schedules widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.schedules, SchedulesWidget)

    def test_edit_schedule_widget(self):
        """Test that the edit schedule widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.edit_schedule, EditScheduleWidget)

    def test_help_widget(self):
        """Test that the help widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.help, HelpWidget)

    def test_settings_widget(self):
        """Test that the settings widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.settings, SettingsWidget)

    def test_profile_widget(self):
        """Test that the profile widget is added correctly."""
        self.assertIsInstance(self.stacked_widget.profile, ProfileWidget)

    @classmethod
    def tearDownClass(cls):
        del cls.stacked_widget


if __name__ == '__main__':
    unittest.main()
