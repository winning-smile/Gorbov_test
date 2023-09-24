from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QPropertyAnimation
import datetime
import button_settings


class AnotherWindow(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(800, 400, 300, 300)
        self.setStyleSheet("background-color: rgb(200,200,200)")
        self.setWindowTitle("Создание карточки пациента")

        self.layout = QVBoxLayout()

        self.first_name_field = QLineEdit()
        self.first_name_field.setPlaceholderText("Имя пациента")

        self.last_name_field = QLineEdit()
        self.last_name_field.setPlaceholderText("Фамилия пациента")

        self.age_field = QLineEdit()
        self.age_field.setPlaceholderText("Возраст пациента")
        self.age_field.setValidator(QIntValidator(1, 99, self))

        self.ok_button = QPushButton("Создать карточку пациента")
        self.ok_button.clicked.connect(self.create_aplicant_profile)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

        self.first_name_field.setStyleSheet(button_settings.menu_lines)
        self.last_name_field.setStyleSheet(button_settings.menu_lines)
        self.age_field.setStyleSheet(button_settings.menu_lines)
        self.ok_button.setStyleSheet(button_settings.menu_button)
        self.exit_button.setStyleSheet(button_settings.menu_button)

        self.layout.addWidget(self.first_name_field)
        self.layout.addWidget(self.last_name_field)
        self.layout.addWidget(self.age_field)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def create_aplicant_profile(self):
        if not self.first_name_field.text() or not self.last_name_field.text() or not self.age_field.text():
            # call exception window from utility.py
            pass

        profile_name = "{0}_{1}.data".format(self.first_name_field.text(), self.last_name_field.text())

        try:
            profile = open(f"data/{profile_name}", "a+")
        except FileNotFoundError:
            profile = open(f"data/{profile_name}", "w+")

        profile.write(self.first_name_field.text()+ '\n')
        profile.write(self.last_name_field.text()+ '\n')
        profile.write(self.age_field.text()+ '\n')
        profile.write("date"+ '\n')
        profile.close()