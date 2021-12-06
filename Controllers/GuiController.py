from GUI.Gui import *
from GUI.WindowProjectAdd import *
from GUI.SettingsDialog import *
import sys

class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindo()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.AddDialog)
        self.ui.stateEditButton.pressed.connect(self.StateDialog)
        self.ui.platformEditBtn.pressed.connect(self.PlatformDialog)

    def AddDialog(self):
        dialog = WindowProjectAdd(self)
        dialog.exec_()
        self.ui.updateTable(True)

    def StateDialog(self):
        dialog = SettingdDialog(self)
        dialog.setType('state')
        dialog.exec_()

    def PlatformDialog(self):
        dialog = SettingdDialog(self)
        dialog.setType('platform')
        dialog.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
