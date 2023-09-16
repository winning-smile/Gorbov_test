from main_tab import *

Black = "rgba(20, 20, 20, 1)"
Red = "rgba(201, 44, 44, 1)"


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.main_tab = MainTab()
        self.output_tab = QWidget()
        self.help_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.main_tab, "Главная")
        self.tabs.addTab(self.output_tab, "Результаты")
        self.tabs.addTab(self.help_tab, "Справка")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
