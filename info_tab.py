from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import utility


class InfoTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.main_layout = QVBoxLayout()
        """Блок с информацией о тесте"""
        self.about = QLabel()
        self.about.setFont(QFont('Arial', 15))
        self.about.setTextFormat(Qt.RichText)
        self.about.setWordWrap(True)
        self.about.setText(utility.info_text)
        self.about.setAlignment(Qt.AlignJustify)
        """Блок с информацией о результатах тестирования"""
        self.results = QLabel()
        self.results.setFont(QFont('Arial', 15))
        self.results.setText("Расшифровка результатов:"
                             "\n>90 секунд: слабое внимание\n"
                             "90-60 секунд: средний уровень внимания\n"
                             "60-30 секунд: хороший уровень внимания\n"
                             "<30 секунд: великолепный уровень внимания\n")

        self.main_layout.addWidget(self.about)
        self.main_layout.addWidget(self.results)
        self.setLayout(self.main_layout)
