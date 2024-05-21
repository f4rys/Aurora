from PyQt6.QtWidgets import QStackedWidget, QSizePolicy

from modules.gui.credentials import CredentialsWidget
from modules.gui.device import DeviceWidget
from modules.gui.all_devices import AllDevicesWidget
from modules.gui.smart_mode import SmartModeWidget
from modules.gui.analytics import AnalyticsWidget
from modules.gui.schedules import SchedulesWidget, EditScheduleWidget
from modules.gui.help import HelpWidget
from modules.gui.settings import SettingsWidget
from modules.gui.profile import ProfileWidget


class StackedWidget(QStackedWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)

        self.credentials = CredentialsWidget(self)
        self.addWidget(self.credentials)

        self.device = DeviceWidget()
        self.addWidget(self.device)

        self.all_devices = AllDevicesWidget(self)
        self.addWidget(self.all_devices)

        self.smart_mode = SmartModeWidget()
        self.addWidget(self.smart_mode)

        self.analytics = AnalyticsWidget(self)
        self.addWidget(self.analytics)

        self.schedules = SchedulesWidget(self)
        self.addWidget(self.schedules)

        self.edit_schedule = EditScheduleWidget(self)
        self.addWidget(self.edit_schedule)

        self.help = HelpWidget()
        self.addWidget(self.help)

        self.settings = SettingsWidget(self)
        self.addWidget(self.settings)

        self.profile = ProfileWidget(self)
        self.addWidget(self.profile)
