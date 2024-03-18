from PyQt6.QtWidgets import QStackedWidget, QSizePolicy

from modules.gui.device import DeviceWidget
from modules.gui.all_devices import AllDevicesWidget
from modules.gui.scenes import ScenesWidget
from modules.gui.analytics import AnalyticsWidget
from modules.gui.schedule import ScheduleWidget
from modules.gui.help import HelpWidget
from modules.gui.settings import SettingsWidget
from modules.gui.profile import ProfileWidget


class StackedWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)

        self.device = DeviceWidget()
        self.addWidget(self.device)

        self.all_devices = AllDevicesWidget()
        self.addWidget(self.all_devices)

        self.scenes = ScenesWidget()
        self.addWidget(self.scenes)

        self.analytics = AnalyticsWidget()
        self.addWidget(self.analytics)

        self.schedule = ScheduleWidget()
        self.addWidget(self.schedule)

        self.help = HelpWidget()
        self.addWidget(self.help)

        self.settings = SettingsWidget()
        self.addWidget(self.settings)

        self.profile = ProfileWidget()
        self.addWidget(self.profile)