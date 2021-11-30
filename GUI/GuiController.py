from GUI.Gui import *
from GUI.WindowProjectAdd import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindo()  # Экземпляр класса Ui_MainWindow, в нем конструктор всего GUI.
        self.ui.setupUi(self)  # Инициализация GUI
        self.ui.pushButton_2.clicked.connect(self.openDialog)  # Открыть новую форму

    def openDialog(self):
        dialog = WindowProjectAdd(self)
        dialog.exec_()

        self.ui.updateTable()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
