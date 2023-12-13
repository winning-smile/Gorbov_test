# Содержит переменные и функции повсеместно встречающиеся по всем участкам кода

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import QPropertyAnimation
import os

import button_settings


Black = "rgba(20, 20, 20, 1)"
Black_initial = QColor(20, 20, 20)
Red = "rgba(201, 44, 44, 1)"
Red_initial = QColor(201, 44, 44)
White = "rgba(255, 255, 255, 1)"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

info_text = """Методика Горбова используется для оценки переключения и распределения
внимания.\nВо время тестирования по данной методике испытуемому последовательно
предъявляются две таблицы, на каждой из которых обозначено 25 красных и 24
черных числа. На первой таблице испытуемый должен указать сначала черные числа в
порядке возрастания, а затем красные числа в порядке убывания. На второй таблице –
попеременно указывать попеременно красные числа в порядке убывания и черные
числа в порядке возрастания.\nЗадача испытуемого – пройти тест как можно быстрее и
с наименьшим количеством ошибок. По окончании прохождения тестирования вычисляется
разница во времени, затраченном на прохождение таблицы номер два и времени,
затраченном на прохождение таблицы номер один. Рассчитанная разница является временем
переключения внимания с одного ряда чисел на другой. Чем меньше рассчитанная
разница, тем лучше показатель переключения внимания у испытуемого."""


def show_warning_messagebox(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def show_results_messagebox(time_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    if time_text > 120:
        msg.setText(f"Ваш результат {time_text} секунд. У вас слабое внимание")
    elif 120 >= time_text > 60:
        msg.setText(f"Ваш результат {time_text} секунд. У вас средний уровень внимания")
    elif 60 >= time_text > 30:
        msg.setText(f"Ваш результат {time_text} секунд. У вас хороший уровень внимания")
    elif time_text < 30:
        msg.setText(f"Ваш результат {time_text} секунд. У вас великолепный уровень внимания")

    msg.setWindowTitle("Результаты")
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
