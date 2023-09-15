from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import datetime

Black = "rgba(20, 20, 20, 1)"
Red = "rgba(201, 44, 44, 1)"

# TODO не забыть прикрутить datetime при сохранении результатов


class Cell(QPushButton):
    """ Класс объекта кнопки с цифрой"""
    def __init__(self, color, val):
        super().__init__()
        self.color = color
        self.vl = val

        self.setAutoFillBackground(True)

        self.setText(str(self.vl))

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.color))
        self.setPalette(palette)

        if color == Black:
            self.setStyleSheet(
            "QPushButton {"
                f"background-color: {color};"
                 "max-height: 60px;"
                 "max-width: 60px;"
                 "margin: 0px;"
                 "padding: 15px;"
                 "color: white;"
                 "font-size: 40px;"
                 "border-radius: 15px;"
                "}"
            "QPushButton::hover {"
                "background-color: rgba(65, 65, 65, 1);"
                "}"
            )
        elif color == Red:
            self.setStyleSheet(
            "QPushButton {"
                f"background-color: {color};"
                 "max-height: 60px;"
                 "max-width: 60px;"
                 "margin: 0px;"
                 "padding: 15px;"
                 "color: white;"
                 "font-size: 40px;"
                 "border-radius: 15px;"
                "}"
            "QPushButton::hover {"
                "background-color: rgba(201, 95, 95, 1);"
                "}"
            )

class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.width_size = 640
        self.height_size = 720
        self.setStyleSheet("background-color: grey;")
        self.setWindowTitle("Gorbov_test")
        self.setGeometry((width-self.width_size)//2, (height-self.height_size)//2, self.width_size, self.height_size)

        self.first_part = False
        self.second_part = False
        self.third_part = False

        self.color_flag = Black
        self.fp = 1
        self.sp = 24

        # Сетка главного окна
        self.main_layout = QGridLayout()

        # Сетка поля с кнопками для исследования
        self.cells_group = QButtonGroup()
        self.cells_layout = QGridLayout()
        self.create_cells()
        self.cells_group.buttonClicked[int].connect(self.on_button_clicked)

        # Сетка с кнопками меню
        self.menu_layout = QGridLayout()

        # Кнопки меню
        self.start_button = QPushButton("Начать исследование")
        self.start_button.clicked.connect(lambda: self.logic_switch("start"))
        self.random_button = QPushButton("Перемешать ячейки")
        self.random_button.clicked.connect(self.shuffle_cells)
        self.stop_button = QPushButton("Остановить исследование")
        self.stop_button.clicked.connect(lambda: self.logic_switch("stop"))
        self.open_button = QPushButton("Открыть директорию с результатами")

        self.name_field = QLineEdit("Введите ваше имя")
        self.age_field = QLineEdit("Введите ваш возраст")

        self.menu_layout.addWidget(self.start_button, 0, 0)
        self.menu_layout.addWidget(self.stop_button, 1, 0)
        self.menu_layout.addWidget(self.random_button, 2, 0)
        self.menu_layout.addWidget(self.open_button, 3, 0)
        self.menu_layout.addWidget(self.name_field, 0, 1, 1, 1)
        self.menu_layout.addWidget(self.age_field, 2, 1, 3, 1)

        cells_widget = QWidget()
        cells_widget.setLayout(self.cells_layout)

        menu_widget = QWidget()
        menu_widget.setLayout(self.menu_layout)

        main_widget = QWidget()
        self.main_layout.addWidget(cells_widget, 0, 0, 6, 6)
        self.main_layout.addWidget(menu_widget, 7, 0, 7, 6)
        main_widget.setLayout(self.main_layout)

        self.setCentralWidget(main_widget)

        self.show()

    def create_cells(self):
        """ Создаём поле с черно-красными карточками в случайном порядке"""
        rng = np.random.default_rng()

        black_numbers = np.arange(1, 26)
        np.random.shuffle(black_numbers)

        red_numbers = np.arange(26, 50)
        np.random.shuffle(red_numbers)
        k = 0
        l = 0

        for i in range(7):
            for j in range(7):
                flag = rng.integers(2)

                if flag % 2 == 0 and k < len(black_numbers):
                    black_button = Cell(Black, black_numbers[k])
                    self.cells_group.addButton(black_button, black_button.vl)
                    self.cells_layout.addWidget(black_button, i, j)
                    k += 1

                elif l < len(red_numbers):
                    red_button = Cell(Red, red_numbers[l]-25)
                    self.cells_group.addButton(red_button, red_button.vl+25)
                    self.cells_layout.addWidget(red_button, i, j)
                    l += 1

                else:
                    black_button = Cell(Black, black_numbers[k])
                    self.cells_group.addButton(black_button, black_button.vl)
                    self.cells_layout.addWidget(black_button, i, j)
                    k += 1

    def logic_switch(self, flag):
        if flag == "start":
            self.random_button.setEnabled(False)
            self.open_button.setEnabled(False)
            self.name_field.setEnabled(False)
            self.age_field.setEnabled(False)

            self.first_part = True
            self.fp = 1
            self.sp = 24

        elif flag == "stop":
            self.random_button.setEnabled(True)
            self.open_button.setEnabled(True)
            self.name_field.setEnabled(True)
            self.age_field.setEnabled(True)

            self.first_part = False
            self.second_part = False
            self.third_part = False

            self.fp = 1
            self.sp = 24

    def shuffle_cells(self):
        for i in reversed(range(self.cells_layout.count())):
            tmp = self.cells_layout.itemAt(i).widget()
            # remove it from the layout list
            self.cells_layout.removeWidget(tmp)
            # remove it from the gui
            tmp.setParent(None)

        self.create_cells()

    def on_button_clicked(self, id):
        if self.first_part:
            print(self.fp)
            print(self.cells_group.button(id).color)
            print(self.cells_group.button(id).vl)
            if self.cells_group.button(id).color == Black and self.cells_group.button(id).vl == self.fp:
                print(f"ok {self.fp}")
                self.fp += 1

            if self.fp == 26:
                self.first_part = False
                self.second_part = True
                self.fp = 49

        if self.second_part:
            print(self.fp)
            print(self.cells_group.button(id).color)
            print(self.cells_group.button(id).vl)

            if self.cells_group.button(id).color == Red and self.cells_group.button(id).vl+25 == self.fp:
                print(f"ok {self.fp}")
                self.fp -= 1

            if self.fp == 25:
                self.second_part = False
                self.third_part = True
                self.fp = 1

        if self.third_part:
            if self.color_flag == Black:
                print("in black")
                if self.cells_group.button(id).color == Black and self.cells_group.button(id).vl == self.fp:
                    print(f"ok {self.fp}")
                    self.fp += 1
                    print("fp= ", self.fp)
                    self.color_flag = Red

            elif self.color_flag == Red:
                print("in red")
                if self.cells_group.button(id).color == Red and self.cells_group.button(id).vl == self.sp:
                    print(f"ok {self.sp}")
                    self.sp -= 1
                    print("fp= ", self.sp)
                    self.color_flag = Black

            if self.fp == 26 and self.sp == 1:
                self.third_part = False
                file_name = self.name_field.text() + self.age_field.text() + str(datetime.date.today()) + ".txt"
                result_file = open(file_name, "x")
                result_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    window = Window(size.width(), size.height())
    sys.exit(app.exec())
