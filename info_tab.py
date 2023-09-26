from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import utility


class InfoTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.main_layout = QVBoxLayout()
        self.about = QLabel()
        self.about.setFont(QFont('Arial', 15))
        self.about.setTextFormat(Qt.RichText)
        self.about.setWordWrap(True)
        self.about.setText(utility.info_text)
        self.about.setAlignment(Qt.AlignJustify)

        self.results = QLabel()
        self.results.setFont(QFont('Arial', 15))
        self.results.setText("Расшифровка результатов:\n<30 секунд: богоподобно\n60-30 секунд: мега-харош\n90-60 секунд: очередняра\n>90 секунд: мега бот")

        self.main_layout.addWidget(self.about)
        self.main_layout.addWidget(self.results)
        self.setLayout(self.main_layout)