from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import datetime
import classes

Black = "rgba(20, 20, 20, 1)"
Red = "rgba(201, 44, 44, 1)"

# TODO не забыть прикрутить datetime при сохранении результатов


class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.width_size = 640
        self.height_size = 720
        self.setStyleSheet("background-color: grey;")
        self.setWindowTitle("Gorbov_test")
        self.setGeometry((width-self.width_size)//2, (height-self.height_size)//2, self.width_size, self.height_size)

        self.tab_widget = classes.TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    window = Window(size.width(), size.height())
    sys.exit(app.exec())
