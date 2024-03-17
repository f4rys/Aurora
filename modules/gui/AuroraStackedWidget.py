from PyQt6.QtWidgets import QStackedWidget, QSizePolicy

from modules.gui.device.DeviceWidget import DeviceWidget
from modules.gui.all_devices.AllDevicesWidget import AllDevicesWidget
from modules.gui.scenes.ScenesWidget import ScenesWidget
from modules.gui.analytics.AnalyticsWidget import AnalyticsWidget
from modules.gui.schedule.ScheduleWidget import ScheduleWidget
from modules.gui.help.HelpWidget import HelpWidget

class AuroraStackedWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)

        self.device = DeviceWidget()
        self.addWidget(self.device)

        self.all_devices = AllDevicesWidget(self)
        self.addWidget(self.all_devices)

        self.scenes = ScenesWidget(self)
        self.addWidget(self.scenes)

        self.analytics = AnalyticsWidget(self)
        self.addWidget(self.analytics)

        self.schedule = ScheduleWidget(self)
        self.addWidget(self.schedule)

        self.help = HelpWidget(self)
        self.addWidget(self.help)