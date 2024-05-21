from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea

from modules.dictionaries.loader import load_dictionary
from modules.resources import resources


class HelpWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dictionary = load_dictionary()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setProperty("class", "borderless")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setEnabled(False) # type: ignore
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_widget.setProperty("class", "borderless")
        self.scroll_area.setWidget(self.scroll_widget)

        self.vlayout = QVBoxLayout(self.scroll_widget)
        self.vlayout.setContentsMargins(10, 0, 15, 0)

        self.faq_label = QLabel("FAQ")
        self.faq_label.setProperty("class", "faq")

        self.tooltips_q_label = QLabel(self.dictionary["tooltips_q"])
        self.tooltips_q_label.setProperty("class", "question")
        self.tooltips_a_label = QLabel(self.dictionary["tooltips_a"])

        self.devices_offline_q_label = QLabel(self.dictionary["devices_offline_q"])
        self.devices_offline_q_label.setProperty("class", "question")
        self.devices_offline_a_label = QLabel(self.dictionary["devices_offline_a"])

        self.countdown_execution_requirements_q_label = QLabel(self.dictionary["countdown_execution_requirements_q"])
        self.countdown_execution_requirements_q_label.setProperty("class", "question")
        self.countdown_execution_requirements_a_label = QLabel(self.dictionary["countdown_execution_requirements_a"])

        self.countdown_limit_q_label = QLabel(self.dictionary["countdown_limit_q"])
        self.countdown_limit_q_label.setProperty("class", "question")
        self.countdown_limit_a_label = QLabel(self.dictionary["countdown_limit_a"])

        self.analytics_plot_q_label = QLabel(self.dictionary["analytics_plot_q"])
        self.analytics_plot_q_label.setProperty("class", "question")
        self.analytics_plot_a_label = QLabel(self.dictionary["analytics_plot_a"])

        self.schedule_error_q_label = QLabel(self.dictionary["schedule_error_q"])
        self.schedule_error_q_label.setProperty("class", "question")
        self.schedule_error_a_label = QLabel(self.dictionary["schedule_error_a"])

        self.schedule_execution_requirements_q_label = QLabel(self.dictionary["schedule_execution_requirements_q"])
        self.schedule_execution_requirements_q_label.setProperty("class", "question")
        self.schedule_execution_requirements_a_label = QLabel(self.dictionary["schedule_execution_requirements_a"])

        self.smart_mode_q_label = QLabel(self.dictionary["smart_mode_q"])
        self.smart_mode_q_label.setProperty("class", "question")
        self.smart_mode_a_label = QLabel(self.dictionary["smart_mode_a"])

        self.question_not_listed_q_label = QLabel(self.dictionary["question_not_listed_q"])
        self.question_not_listed_q_label.setProperty("class", "question")
        self.question_not_listed_a_1_label = QLabel(self.dictionary["question_not_listed_a_1"])
        self.email_label = QLabel()
        self.email_label.setProperty("class", "link")
        self.email_label.setText("<a href='"'mailto:wojciech.michal.bartoszek@gmail.com'"'>wojciech.michal.bartoszek@gmail.com</a")
        self.email_label.setOpenExternalLinks(True)
        self.question_not_listed_a_2_label = QLabel(self.dictionary["question_not_listed_a_2"])
        self.repository_label = QLabel()
        self.repository_label.setProperty("class", "link")
        self.repository_label.setText("<a href='https://github.com/f4rys/Aurora'>https://github.com/f4rys/Aurora</a>")
        self.repository_label.setOpenExternalLinks(True)

        self.icon_label = QLabel()
        self.icon_label.setObjectName("app_icon")
        self.icon_label.setPixmap(QIcon(":/icon/icon.png").pixmap(QSize(32, 32)))

        self.project_label = QLabel("Aurora v1.0.0")
        self.author_label = QLabel(self.dictionary["author"] + " Wojciech Bartoszek")

        self.vlayout.addWidget(self.faq_label)
        self.vlayout.addWidget(self.tooltips_q_label)
        self.vlayout.addWidget(self.tooltips_a_label)
        self.vlayout.addWidget(self.devices_offline_q_label)
        self.vlayout.addWidget(self.devices_offline_a_label)
        self.vlayout.addWidget(self.countdown_execution_requirements_q_label)
        self.vlayout.addWidget(self.countdown_execution_requirements_a_label)
        self.vlayout.addWidget(self.countdown_limit_q_label)
        self.vlayout.addWidget(self.countdown_limit_a_label)
        self.vlayout.addWidget(self.analytics_plot_q_label)
        self.vlayout.addWidget(self.analytics_plot_a_label)
        self.vlayout.addWidget(self.schedule_error_q_label)
        self.vlayout.addWidget(self.schedule_error_a_label)
        self.vlayout.addWidget(self.schedule_execution_requirements_q_label)
        self.vlayout.addWidget(self.schedule_execution_requirements_a_label)
        self.vlayout.addWidget(self.smart_mode_q_label)
        self.vlayout.addWidget(self.smart_mode_a_label)
        self.vlayout.addWidget(self.question_not_listed_q_label)
        self.vlayout.addWidget(self.question_not_listed_a_1_label)
        self.vlayout.addWidget(self.email_label)
        self.vlayout.addWidget(self.question_not_listed_a_2_label)
        self.vlayout.addWidget(self.repository_label)
        self.vlayout.addWidget(self.icon_label)
        self.vlayout.addWidget(self.project_label)
        self.vlayout.addWidget(self.author_label)
