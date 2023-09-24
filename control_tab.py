from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QPropertyAnimation
import numpy as np
import datetime
import button_settings


class ControlTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()