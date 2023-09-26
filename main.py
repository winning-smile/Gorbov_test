from PyQt5.QtWidgets import *
import sys

import tab_widget


class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.width_size = 640
        self.height_size = 720
        self.setStyleSheet("background-color: rgb(200,200,200)")
        self.setWindowTitle("Тест Горбова")
        self.setGeometry((width-self.width_size)//2, (height-self.height_size)//2, self.width_size, self.height_size)
        self.setFixedSize(self.width_size, self.height_size+80)

        self.tab_widget = tab_widget.TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    # Инициализация приложения
    window = Window(size.width(), size.height())
    sys.exit(app.exec())
