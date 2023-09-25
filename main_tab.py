from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import button_settings
from cells_generator import create_normalize_matrix
import create_applicant_window as caw
import utility
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# TODO comments, split timers, split tables for 1/2 stage , code refactor
# DONE section for 1 and 2 stage, new shuffle logic


class MainTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        # Флаги и переменные для разметки этапов тестирования
        self.first_part = False
        self.second_part = False
        self.third_part = False
        self.color_flag = utility.Black
        self.shuffle_once_flag = False
        self.fp = 1
        self.sp = 24
        self.errors = 0

        # Окно создания карточки пациента
        self.create_window = None

        # Таймер
        self.timer = QTimer()
        self.timer_flag = False
        self.count = 0
        self.timer.timeout.connect(self.show_time)
        self.timer.start(100)
        self.first_part_time = 0
        self.second_part_time = 0

        # Разметка окна
        self.setup_ui()
        self.update_apllicant_base()

    def setup_ui(self):
        # Сетка главного окна
        self.main_layout = QGridLayout()
        self.cells_layout = QGridLayout()
        self.menu_layout = QGridLayout()

        self.cells_widget = QWidget()
        self.cells_widget.setLayout(self.cells_layout)
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)

        self.cells_group = QButtonGroup()
        self.create_cells()
        self.cells_group.buttonClicked[int].connect(self.on_button_clicked)

        self.menu_group = QButtonGroup()

        # Кнопки меню
        self.start_button = QPushButton("Начать тест")
        self.start_button.clicked.connect(lambda: self.logic_switch("start"))

        self.random_button = QPushButton("Перемешать ячейки")
        self.random_button.clicked.connect(self.shuffle_cells)

        self.stop_button = QPushButton("Остановить тест")
        self.stop_button.clicked.connect(lambda: self.logic_switch("stop"))

        self.chose_applicant_label = QComboBox()
        self.chose_applicant_label.setStyleSheet(button_settings.chose_line)

        self.create_applicant_button = QPushButton("Новый испытуемый")
        self.create_applicant_button.clicked.connect(lambda: self.create_applicant())

        self.update_apllicant_button = QPushButton("Обновить базу")
        self.update_apllicant_button.clicked.connect(lambda: self.update_apllicant_base())

        self.timer_label = QLabel("0:00")
        self.timer_label.setFont(QFont('Times', 30))
        self.timer_label.setAlignment(Qt.AlignLeft)

        self.group_menu_buttons()

        self.menu_layout.addWidget(self.start_button, 0, 0)
        self.menu_layout.addWidget(self.stop_button, 1, 0)
        self.menu_layout.addWidget(self.random_button, 2, 0)
        self.menu_layout.addWidget(self.timer_label, 1, 1, 2, 2)
        self.menu_layout.addWidget(self.chose_applicant_label, 0, 1)
        self.menu_layout.addWidget(self.create_applicant_button, 0, 2)
        self.menu_layout.addWidget(self.update_apllicant_button, 1, 2)

        self.main_widget = QWidget()
        self.main_layout.addWidget(self.cells_widget, 0, 0, 6, 6)
        self.main_layout.addWidget(self.menu_widget, 7, 0, 7, 6)
        self.main_widget.setLayout(self.main_layout)

        self.setLayout(self.main_layout)

    def group_menu_buttons(self):
        self.menu_group.addButton(self.start_button)
        self.menu_group.addButton(self.stop_button)
        self.menu_group.addButton(self.random_button)
        self.menu_group.addButton(self.create_applicant_button)
        self.menu_group.addButton(self.update_apllicant_button)

        for button in self.menu_group.buttons():
            button.setStyleSheet(button_settings.menu_button)

    def create_cells(self):
        """ Создаём поле с черно-красными карточками в неслучайном случайном порядке"""
        matrix = create_normalize_matrix()

        for i in range(len(matrix)):
            if matrix[i] <= 25:
                black_button = utility.Cell(utility.Black, matrix[i])
                self.cells_group.addButton(black_button, black_button.vl)
                self.cells_layout.addWidget(black_button, i//7, i % 7)
            else:
                red_button = utility.Cell(utility.Red, matrix[i] - 25)
                self.cells_group.addButton(red_button, red_button.vl + 25)
                self.cells_layout.addWidget(red_button, i//7, i % 7)

    def logic_switch(self, flag):
        if flag == "start":
            self.count = 0
            self.random_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.create_applicant_button.setEnabled(False)
            self.update_apllicant_button.setEnabled(False)
            self.chose_applicant_label.setEnabled(False)
            self.first_part = True
            self.fp = 1
            self.sp = 24
            utility.show_info_messagebox("Последовательно нажмите на чёрные числа в порядке возрастания")

        elif flag == "stop":
            self.start_button.setEnabled(True)
            self.random_button.setEnabled(True)
            self.create_applicant_button.setEnabled(True)
            self.update_apllicant_button.setEnabled(True)
            self.chose_applicant_label.setEnabled(True)
            self.first_part = False
            self.second_part = False
            self.third_part = False
            self.shuffle_once_flag = False
            self.fp = 1
            self.sp = 24
            self.timer_flag = False
            self.count = 0

        elif flag == "reset":
            self.errors = 0

    def create_applicant(self):
        if self.create_window is None:
            self.create_window = caw.CreateApplicantWindow()
        self.create_window.exec()

    def update_apllicant_base(self):
        self.chose_applicant_label.clear()
        applicants = []

        for profile in os.listdir(ROOT_DIR+"/data"):
            applicants.append(profile[:-5])

        for profile in applicants:
            self.chose_applicant_label.addItem(profile)

    def shuffle_cells(self):
        for i in reversed(range(self.cells_layout.count())):
            tmp = self.cells_layout.itemAt(i).widget()
            self.cells_layout.removeWidget(tmp)
            tmp.setParent(None)
            tmp.deleteLater()
        self.create_cells()

    def on_button_clicked(self, button_id):
        self.current_aplicant = self.chose_applicant_label.currentText()

        if self.first_part:
            if self.cells_group.button(button_id).initial_color == utility.Black and self.cells_group.button(button_id).vl == self.fp:
                if not self.timer_flag:
                    self.timer_flag = True
                    self.show_time()

                self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                self.fp += 1

            else:
                self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)
                self.errors += 1

            if self.fp == 26:
                self.first_part = False
                self.second_part = True
                self.fp = 49
                self.timer_flag = False
                utility.show_info_messagebox("Последовательно нажмите на красные числа в порядке убывания")

        if self.second_part:
            if self.cells_group.button(button_id).initial_color == utility.Red and self.cells_group.button(button_id).vl + 25 == self.fp:
                if not self.timer_flag:
                    self.timer_flag = True

                self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                self.fp -= 1

            else:
                self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)
                self.errors += 1

            if self.fp == 25:
                self.first_part_time = self.count/10
                self.second_part = False
                self.third_part = True
                self.fp = 1
                self.timer_flag = False
                utility.show_info_messagebox("Поочерёдно нажимайте на чёрные числа в порядке возрастания, а красные в порядке убывания")

        if self.third_part:

            if not self.shuffle_once_flag:
                self.shuffle_cells()
                self.shuffle_once_flag = True

            if self.color_flag == utility.Black:
                if self.cells_group.button(button_id).initial_color == utility.Black and self.cells_group.button(button_id).vl == self.fp:
                    if not self.timer_flag:
                        self.timer_flag = True
                    self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                    self.fp += 1
                    self.color_flag = utility.Red

                else:
                    self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)
                    self.errors += 1

            elif self.color_flag == utility.Red:
                if self.cells_group.button(button_id).initial_color == utility.Red and self.cells_group.button(button_id).vl == self.sp:
                    self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                    self.sp -= 1
                    self.color_flag = utility.Black

                else:
                    self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)
                    self.errors += 1

            if self.fp == 26 and self.sp == 0:
                self.second_part_time = (self.count/10) - self.first_part_time
                self.timer_flag = False
                self.third_part = False
                self.logic_switch("stop")

                profile = open(ROOT_DIR + f"/data/{self.current_aplicant}.data", "a+")
                profile.write(f"{self.second_part_time - self.first_part_time}\n {self.errors-2}")
                self.logic_switch("reset")

    def show_time(self):
        if self.timer_flag:
            self.count += 1

        text = str(self.count / 10)
        self.timer_label.setText(text)
