from PyQt6.QtWidgets import QStackedWidget, QSizePolicy

from modules.gui import DeviceWidget, AllDevicesWidget, ScenesWidget, AnalyticsWidget, ScheduleWidget, HelpWidget


class AuroraStackedWidget(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)

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