from PyQt5.QtWidgets import *
import button_settings
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import utility
import os

class ListIterator():
    def __init__(self):
        self.values = ["times", "errors", "date"]
        self.current_value = "date"
        self.count = 0

    def next_current_value(self):
        self.current_value = self.values[self.count % 3]
        self.count += 1

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=6, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, position=[0.15, 0.15, 0.75, 0.75])
        super(MplCanvas, self).__init__(fig)


class OutputTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.errors = []
        self.times = []
        self.dates = []
        self.logic_flags = ["date", "times", "errors"]
        self.logic_flag = "date"
        self.setup_ui()
        self.update_apllicant_base()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.menu_layout = QHBoxLayout()
        self.graph_layout = QVBoxLayout()

        self.menu_widget = QWidget()
        self.graph_widget = QWidget()

        self.chose_applicant_label = QComboBox()
        self.chose_applicant_label.setStyleSheet(button_settings.chose_line)
        self.show_results_button = QPushButton("Показать результаты")
        self.show_results_button.clicked.connect(lambda: self.show_results())
        self.show_results_button.setStyleSheet(button_settings.menu_button)
        self.update_applicants_base_button = QPushButton("Обновить базу")
        self.update_applicants_base_button.clicked.connect(lambda: self.update_apllicant_base())
        self.update_applicants_base_button.setStyleSheet(button_settings.menu_button)

        self.main_graph = MplCanvas(self, width=5, height=4, dpi=100)
        self.additional_graph = MplCanvas(self, width=5, height=4, dpi=100)

        self.menu_layout.addWidget(self.chose_applicant_label)
        self.menu_layout.addWidget(self.show_results_button)
        self.menu_layout.addWidget(self.update_applicants_base_button)

        self.graph_layout.addWidget(self.main_graph)
        self.graph_layout.addWidget(self.additional_graph)

        self.menu_widget.setLayout(self.menu_layout)
        self.graph_widget.setLayout(self.graph_layout)

        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.graph_widget)

        self.setLayout(self.main_layout)

    def input_logic(self, flag, value):
        if flag == "times":
            self.times.append(float(value))
        elif flag == "errors":
            self.errors.append(int(value))
        elif flag == "date":
            self.dates.append(str(value)[:-1])

    def add_mark_to_graph(self):
        self.main_graph.axes.axhline(y=30, color="green", linestyle='--')
        self.main_graph.axes.axhline(y=60, color="yellow", linestyle='--')
        self.main_graph.axes.axhline(y=90, color="red", linestyle='--')

    def show_results(self):
        self.dates = []
        self.times = []
        self.errors = []
        self.main_graph.axes.cla()
        self.additional_graph.axes.cla()

        list_iterator = ListIterator()
        count = 0
        profile_name = self.chose_applicant_label.currentText()

        try:
            profile = open(utility.ROOT_DIR+"/data/"+profile_name+".data", "r")

            for line in profile:
                if count < 3:
                    count += 1
                    continue

                else:
                    self.input_logic(list_iterator.current_value, line)
                    list_iterator.next_current_value()

        finally:
            profile.close()
            del list_iterator


        self.main_graph.axes.plot(self.dates, self.times, color="black")
        self.main_graph.axes.set_xlabel("Дата тестирования")
        self.main_graph.axes.set_ylabel("Время, с.")
        self.add_mark_to_graph()
        self.additional_graph.axes.plot(self.dates, self.errors, color="black")
        self.additional_graph.axes.set_xlabel("Дата тестирования")
        self.additional_graph.axes.set_ylabel("Кол-во ошибок")


        self.main_graph.draw()
        self.additional_graph.draw()

    def update_apllicant_base(self):
        self.chose_applicant_label.clear()
        applicants = []

        for profile in os.listdir(utility.ROOT_DIR+"/data"):
            applicants.append(profile[:-5])

        for profile in applicants:
            self.chose_applicant_label.addItem(profile)