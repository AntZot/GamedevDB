from GUI.Gui import *
from GUI.WindowProjectAdd import *
import sys

class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindo()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.AddDialog)

    def AddDialog(self):
        dialog = WindowProjectAdd(self)
        dialog.exec_()
        self.ui.updateTable(True)

    def StateDialog(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
