from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import QPropertyAnimation
import button_settings

Black = "rgba(20, 20, 20, 1)"
Black_initial = QColor(20, 20, 20)
Red = "rgba(201, 44, 44, 1)"
Red_initial = QColor(201, 44, 44)
White = "rgba(255, 255, 255, 1)"


def show_warning_messagebox(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
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
