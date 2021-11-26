from dbController import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):  # если собрался передавать аргументы, то не забудь их принять (nameofargument, self, parent=None)
        super().__init__(parent, QtCore.Qt.Window)
        self.build()  # ну и передать в открывающееся окно соответственно (nameofargument, self)

    def build(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('NoTittle')

