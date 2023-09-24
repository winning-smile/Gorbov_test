from main_tab import *
from control_tab import ControlTab
from output_tab import OutputTab
from info_tab import InfoTab


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.main_tab = MainTab()
        self.output_tab = OutputTab()
        self.info_tab = InfoTab()
        self.control_tab = ControlTab()

        # Add tabs
        self.tabs.addTab(self.main_tab, "Главная")
        self.tabs.addTab(self.control_tab, "Панель управления")
        self.tabs.addTab(self.output_tab, "Результаты")
        self.tabs.addTab(self.info_tab, "Справка")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
