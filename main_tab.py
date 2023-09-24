from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QPropertyAnimation
import numpy as np
import datetime
import button_settings
from cells_generator import create_normalize_matrix

# TODO comments, split timers, new shuffle logic, split tables for 1/2 stage , code refactor
# DONE section for 1 and 2 stage

Black = "rgba(20, 20, 20, 1)"
Black_initial = QColor(20, 20, 20)
Red = "rgba(201, 44, 44, 1)"
Red_initial = QColor(201, 44, 44)
White = "rgba(255, 255, 255, 1)"


def show_warning_messagebox():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Для запуска теста введите ваше имя и возраст")
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def show_info_messagebox(text):
    """ Всплывающее окно с инструкциями к тесту"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Инструкция")
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class Cell(QPushButton):
    """ Класс объекта кнопки с цифрой"""
    def __init__(self, initial_color, val):
        super().__init__()
        self.initial_color = initial_color
        self.vl = val
        self.init_style_sheet = None
        self.setAutoFillBackground(True)
        self.setText(str(self.vl))

        if self.initial_color == Black:
            self.color_anim = Black_initial
            self.init_style_sheet = button_settings.black_default
            self.setStyleSheet(button_settings.black_default)

        elif self.initial_color == Red:
            self.color_anim = Red_initial
            self.init_style_sheet = button_settings.red_default
            self.setStyleSheet(button_settings.red_default)

        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'color_anim')
        self.animation.finished.connect(self.clear_style_sheet)

    def clear_style_sheet(self):
        self.setStyleSheet(self.init_style_sheet)

    @pyqtProperty(QColor)
    def color_anim(self):
        return self._color_anim

    @color_anim.setter
    def color_anim(self, color):
        self._color_anim = color
        new_style = f"background-color: {color.name()};"
        merged_style = f'{self.init_style_sheet}\n{new_style}'
        self.setStyleSheet(merged_style)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def animate_color(self, end_color, duration):
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(duration)
        self.animation.setStartValue(end_color)
        if self.initial_color == Black:
            self.animation.setEndValue(Black_initial)
        else:
            self.animation.setEndValue(Red_initial)
        self.animation.start()


class MainTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.first_part = False
        self.second_part = False
        self.third_part = False

        # Таймер
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

        self.bs = 0
        self.rs = 0

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

        self.timer_label = QLabel("0:00")
        self.timer_label.setFont(QFont('Times', 30))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.group_menu_buttons()

        self.menu_layout.addWidget(self.start_button, 0, 0)
        self.menu_layout.addWidget(self.stop_button, 1, 0)
        self.menu_layout.addWidget(self.random_button, 2, 0)
        self.menu_layout.addWidget(self.timer_label, 0, 2, 2, 2)

        self.main_widget = QWidget()
        self.main_layout.addWidget(self.cells_widget, 0, 0, 6, 6)
        self.main_layout.addWidget(self.menu_widget, 7, 0, 7, 6)
        self.main_widget.setLayout(self.main_layout)

        self.setLayout(self.main_layout)

    def group_menu_buttons(self):
        self.menu_group.addButton(self.start_button)
        self.menu_group.addButton(self.stop_button)
        self.menu_group.addButton(self.random_button)

        for button in self.menu_group.buttons():
            button.setStyleSheet(button_settings.menu_button)

    def cells_distance(self, bl, rl):
        black_sum = 0
        red_sum = 0

        for i in range(1, len(bl)):
            black_sum += np.sqrt((bl[i-1][1] - bl[i][1])**2 + (bl[i-1][2] - bl[i][2])**2)

        for i in range(1, len(rl)):
            red_sum += np.sqrt((rl[i-1][1] - rl[i][1])**2 + (rl[i-1][2] - rl[i][2])**2)

        return black_sum, red_sum

    def create_cells(self):
        """ Создаём поле с черно-красными карточками в неслучайном случайном порядке"""
        matrix = create_normalize_matrix()

        for i in range(len(matrix)):
            if matrix[i] <= 25:
                black_button = Cell(Black, matrix[i])
                self.cells_group.addButton(black_button, black_button.vl)
                self.cells_layout.addWidget(black_button, i//7, i%7)
            else:
                red_button = Cell(Red, matrix[i] - 25)
                self.cells_group.addButton(red_button, red_button.vl + 25)
                self.cells_layout.addWidget(red_button, i//7, i%7)

    def logic_switch(self, flag):
        if flag == "start":
            self.count = 0
            self.random_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.first_part = True
            self.fp = 1
            self.sp = 24
            show_info_messagebox("Последовательно нажмите на чёрные числа в порядке возрастания")

        elif flag == "stop":
            self.start_button.setEnabled(True)
            self.random_button.setEnabled(True)
            self.first_part = False
            self.second_part = False
            self.third_part = False
            self.fp = 1
            self.sp = 24
            self.timer_flag = False
            self.count = 0

    def shuffle_cells(self):
        for i in reversed(range(self.cells_layout.count())):
            tmp = self.cells_layout.itemAt(i).widget()
            self.cells_layout.removeWidget(tmp)
            tmp.setParent(None)
            tmp.deleteLater()
        self.create_cells()

    # TODO Button 25 animation white?
    def on_button_clicked(self, button_id):
        if self.first_part:
            if self.cells_group.button(button_id).initial_color == Black and self.cells_group.button(button_id).vl == self.fp:
                if not self.timer_flag:
                    self.timer_flag = True
                    self.show_time()

                self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                self.fp += 1

            else:
                self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)

            if self.fp == 26:
                self.first_part = False
                self.second_part = True
                self.fp = 49
                self.timer_flag = False
                show_info_messagebox("Последовательно нажмите на красные числа в порядке убывания")

        # TODO Переделать на self.sp для красных
        if self.second_part:
            if self.cells_group.button(button_id).initial_color == Red and self.cells_group.button(button_id).vl + 25 == self.fp:
                if not self.timer_flag:
                    self.timer_flag = True

                self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                self.fp -= 1

            else:
                self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)

            if self.fp == 25:
                self.first_part_time = self.count/10
                self.second_part = False
                self.third_part = True
                self.fp = 1
                self.timer_flag = False
                show_info_messagebox("Поочерёдно нажимайте на чёрные числа в порядке возрастания, а красные в порядке убывания")

        if self.third_part:
            if self.color_flag == Black:
                if self.cells_group.button(button_id).initial_color == Black and self.cells_group.button(button_id).vl == self.fp:
                    if not self.timer_flag:
                        self.timer_flag = True
                    self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                    self.fp += 1
                    self.color_flag = Red

                else:
                    self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)

            elif self.color_flag == Red:
                if self.cells_group.button(button_id).initial_color == Red and self.cells_group.button(button_id).vl == self.sp:
                    self.cells_group.button(button_id).animate_color(QColor("green"), duration=900)
                    self.sp -= 1
                    self.color_flag = Black

                else:
                    self.cells_group.button(button_id).animate_color(QColor("white"), duration=900)

            if self.fp == 26 and self.sp == 0:
                self.second_part_time = (self.count/10) - self.first_part_time
                self.timer_flag = False
                self.third_part = False
                self.logic_switch("stop")

    def show_time(self):
        if self.timer_flag:
            self.count += 1

        text = str(self.count / 10)
        self.timer_label.setText(text)