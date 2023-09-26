from main_tab import *
from output_tab import OutputTab
from info_tab import InfoTab


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Инициализация вкладок
        self.tabs = QTabWidget()
        # Основная вкладка с тестом
        self.main_tab = MainTab()
        # Вкладка с результатами
        self.output_tab = OutputTab()
        # Вкладка со справочной информацией
        self.info_tab = InfoTab()

        self.tabs.addTab(self.main_tab, "Главная")
        self.tabs.addTab(self.output_tab, "Результаты")
        self.tabs.addTab(self.info_tab, "Справка")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
