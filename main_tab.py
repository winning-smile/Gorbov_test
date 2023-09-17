from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import numpy as np
import datetime
import button_settings

Black = "rgba(20, 20, 20, 1)"
Red = "rgba(201, 44, 44, 1)"


def show_warning_messagebox():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Для запуска теста введите ваше имя и возраст")
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def show_info_messagebox():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Инструкция")
    msg.setText("Для прохождения теста необходимо:\n1. Последовательно выбрать чёрные числа в порядке возрастания\n2. Последовательно выбрать красные числа в порядке убывания\n3. Поочерёдно выбрать черные числа в порядке возрастания и красные в порядке убывания")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class Cell(QPushButton):
    """ Класс объекта кнопки с цифрой"""
    def __init__(self, color, val):
        super().__init__()
        self.color = color
        self.vl = val

        self.setAutoFillBackground(True)

        self.setText(str(self.vl))

        if color == Black:
            self.setStyleSheet(button_settings.black_default)
        elif color == Red:
            self.setStyleSheet(button_settings.red_default)


class MainTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.first_part = False
        self.second_part = False
        self.third_part = False

        self.timer = QTimer()
        self.timer_flag = False
        self.count = 0
        self.timer.timeout.connect(self.show_time)
        self.timer.start(100)

        self.color_flag = Black
        self.buttons_color_mode = "Colorfull"
        self.fp = 1
        self.sp = 24

        self.first_part_time = 0
        self.second_part_time = 0

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

        self.open_button = QPushButton("Открыть результаты")

        self.change_color_button = QPushButton("Изменить цветовой стиль")
        self.change_color_button.clicked.connect(lambda: self.logic_switch("change_color"))

        self.timer_label = QLabel("0:00")
        self.timer_label.setFont(QFont('Times', 30))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Введите ваше имя")
        self.age_field = QLineEdit()
        self.age_field.setPlaceholderText("Введите ваш возраст")

        self.group_menu_buttons()

        self.menu_layout.addWidget(self.start_button, 0, 0)
        self.menu_layout.addWidget(self.stop_button, 1, 0)
        self.menu_layout.addWidget(self.random_button, 2, 0)
        self.menu_layout.addWidget(self.open_button, 3, 0)
        self.menu_layout.addWidget(self.name_field, 0, 1)
        self.menu_layout.addWidget(self.age_field, 1, 1)
        self.menu_layout.addWidget(self.timer_label, 0, 2, 2, 2)
        self.menu_layout.addWidget(self.change_color_button, 3, 1)

        self.main_widget = QWidget()
        self.main_layout.addWidget(self.cells_widget, 0, 0, 6, 6)
        self.main_layout.addWidget(self.menu_widget, 7, 0, 7, 6)
        self.main_widget.setLayout(self.main_layout)

        self.setLayout(self.main_layout)

    def group_menu_buttons(self):
        self.menu_group.addButton(self.start_button)
        self.menu_group.addButton(self.stop_button)
        self.menu_group.addButton(self.random_button)
        self.menu_group.addButton(self.change_color_button)
        self.menu_group.addButton(self.open_button)

        for button in self.menu_group.buttons():
            button.setStyleSheet(button_settings.menu_button)

        self.name_field.setStyleSheet(button_settings.menu_lines)
        self.age_field.setStyleSheet(button_settings.menu_lines)

    def create_cells(self):
        """ Создаём поле с черно-красными карточками в случайном порядке"""
        rng = np.random.default_rng()
        black_numbers = np.arange(1, 26)
        np.random.shuffle(black_numbers)
        red_numbers = np.arange(26, 50)
        np.random.shuffle(red_numbers)
        black_iterator = 0
        red_iterator = 0
        for i in range(7):
            for j in range(7):
                flag = rng.integers(2)
                if flag % 2 == 0 and black_iterator < len(black_numbers):
                    black_button = Cell(Black, black_numbers[black_iterator])
                    self.cells_group.addButton(black_button, black_button.vl)
                    self.cells_layout.addWidget(black_button, i, j)
                    black_iterator += 1
                elif red_iterator < len(red_numbers):
                    red_button = Cell(Red, red_numbers[red_iterator] - 25)
                    self.cells_group.addButton(red_button, red_button.vl + 25)
                    self.cells_layout.addWidget(red_button, i, j)
                    red_iterator += 1
                else:
                    black_button = Cell(Black, black_numbers[black_iterator])
                    self.cells_group.addButton(black_button, black_button.vl)
                    self.cells_layout.addWidget(black_button, i, j)
                    black_iterator += 1

    def logic_switch(self, flag):
        if flag == "start":
            if not self.name_field.text() and not self.age_field.text():
                show_warning_messagebox()
            else:
                self.count = 0
                self.random_button.setEnabled(False)
                self.open_button.setEnabled(False)
                self.name_field.setEnabled(False)
                self.age_field.setEnabled(False)
                self.change_color_button.setEnabled(False)
                self.start_button.setEnabled(False)
                self.first_part = True
                self.fp = 1
                self.sp = 24
                show_info_messagebox()

        elif flag == "stop":
            self.start_button.setEnabled(True)
            self.random_button.setEnabled(True)
            self.open_button.setEnabled(True)
            self.name_field.setEnabled(True)
            self.age_field.setEnabled(True)
            self.change_color_button.setEnabled(True)
            self.first_part = False
            self.second_part = False
            self.third_part = False
            self.fp = 1
            self.sp = 24
            self.timer_flag = False
            self.count = 0

        elif flag == "change_color":
            if self.buttons_color_mode == "Colorfull":
                for button in self.cells_group.buttons():
                    if button.color == Black:
                        button.setStyleSheet(button_settings.black_white)
                    else:
                        button.setStyleSheet(button_settings.red_white)

                self.buttons_color_mode = "White"

            else:
                for button in self.cells_group.buttons():
                    if button.color == Black:
                        button.setStyleSheet(button_settings.black_default)
                    else:
                        button.setStyleSheet(button_settings.red_default)

                self.buttons_color_mode = "Colorfull"

    def shuffle_cells(self):
        for i in reversed(range(self.cells_layout.count())):
            tmp = self.cells_layout.itemAt(i).widget()
            self.cells_layout.removeWidget(tmp)
            tmp.setParent(None)
        self.create_cells()

    def on_button_clicked(self, button_id):
        if self.first_part:
            if self.cells_group.button(button_id).color == Black and self.cells_group.button(button_id).vl == self.fp:
                if not self.timer_flag:
                    self.timer_flag = True
                    self.show_time()

                self.fp += 1

            if self.fp == 26:
                self.first_part = False
                self.second_part = True
                self.fp = 49

        if self.second_part:
            if self.cells_group.button(button_id).color == Red and self.cells_group.button(button_id).vl + 25 == self.fp:
                self.fp -= 1

            if self.fp == 25:
                self.first_part_time = self.count/10
                self.second_part = False
                self.third_part = True
                self.fp = 1

        if self.third_part:
            if self.color_flag == Black:
                if self.cells_group.button(button_id).color == Black and self.cells_group.button(button_id).vl == self.fp:
                    self.fp += 1
                    self.color_flag = Red

            elif self.color_flag == Red:
                if self.cells_group.button(button_id).color == Red and self.cells_group.button(button_id).vl == self.sp:
                    self.sp -= 1
                    self.color_flag = Black

            if self.fp == 26 and self.sp == 0:
                self.second_part_time = (self.count/10) - self.first_part_time
                self.timer_flag = False
                self.third_part = False
                file_name = self.name_field.text() + "_" + self.age_field.text() + "_" + str(datetime.date.today()) + ".txt"
                result_file = open(file_name, "x")
                result_file.write(f"1 часть = {self.first_part_time} секунд")
                result_file.write(f"2 часть = {self.second_part_time} секунд")
                result_file.write(f"разница = {self.second_part_time - self.first_part_time} секунд")
                result_file.close()

    def show_time(self):
        if self.timer_flag:
            # incrementing the counter
            self.count += 1
            # getting text from count
        text = str(self.count / 10)

        # showing text
        self.timer_label.setText(text)
