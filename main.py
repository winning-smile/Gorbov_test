from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np

# TODO не забыть прикрутить datetime при сохранении результатов

class Cell(QPushButton):
    """ Класс объекта кнопки с цифрой"""
    def __init__(self, color, val, x, y):
        super().__init__()
        self.color = color
        self.vl = val
        self.x = x
        self.y = y

        self.setAutoFillBackground(True)

        self.setText(str(self.vl))

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.color))
        self.setPalette(palette)

        if color == "rgba(20, 20, 20, 1)":
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
        elif color == "rgba(201, 44, 44, 1)":
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

        # Сетка главного окна
        self.main_layout = QGridLayout()

        # Сетка поля с кнопками для исследования
        self.cells_layout = QGridLayout()
        self.create_cells()

        # Сетка с кнопками меню
        self.menu_layout = QGridLayout()

        # Кнопки меню
        self.start_button = QPushButton("Начать исследование")
        self.random_button = QPushButton("Перемешать ячейки")
        self.stop_button = QPushButton("Остановить исследование")
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
        rng = np.random.default_rng(2)

        black_numbers = np.arange(1, 26)
        np.random.shuffle(black_numbers)

        red_numbers = np.arange(1, 25)
        np.random.shuffle(red_numbers)
        k = 0
        l = 0

        for i in range(7):
            for j in range(7):
                flag = rng.integers(2)

                if flag % 2 == 0 and k < len(black_numbers):
                    self.cells_layout.addWidget(Cell("rgba(20, 20, 20, 1)", black_numbers[k], 1, 1), i, j)
                    k += 1

                elif l < len(red_numbers):
                    self.cells_layout.addWidget(Cell("rgba(201, 44, 44, 1)", red_numbers[l], 1, 1), i, j)
                    l += 1

                else:
                    self.cells_layout.addWidget(Cell("rgba(20, 20, 20, 1)", black_numbers[k], 1, 1), i, j)
                    k += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    window = Window(size.width(), size.height())
    sys.exit(app.exec())
