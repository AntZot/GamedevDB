from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from datetime import date
import sys
import dbController

"""Db = dbController

    Connection = Db.create_connection()
    cursor = Connection.cursor()
    cursor.execute("show tables;")
    for db in cursor:
        print(db)
    g = GUI.Gui
    g.gui()"""

Connection = dbController.create_connection()

cursor = Connection.cursor()

stylesheet = """
    QWidget{
        background-color: white;
    }

    QWidget#sideMenuBackground{
        background-color: #f7f7f7;
    }

    QVBoxLayout#sideMenuLayout{
        background-color: grey;
    }


    QPushButton#sideMenuButton{
        text-align: left;
        border: none;
        background-color: #f7f7f7;
        max-width: 10em;
        font: 16px; 
        padding: 6px;
    }

    QPushButton#sideMenuButton:hover{
        font: 18px;
    }

    QLabel#project_base_label{
        font: 25px;

    }

    QLabel#todays_date_label{
        font: 11px;
        color: grey;
    }

    QPushButton#addTodoEventButton{
    }


"""


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gamedev project base")
        self.setGeometry(200, 200, 900, 780)
        self.initUI()

    def initUI(self):

        self.nextWeekPage = QtWidgets.QLabel()

        backgroundWidget = QtWidgets.QWidget()
        backgroundWidget.setObjectName("sideMenuBackground")
        backgroundWidget.setFixedWidth(150)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(backgroundWidget)
        sideMenuLayout = QtWidgets.QVBoxLayout()
        sideMenuLayout.setObjectName("sideMenuLayout")
        self.taskLayout = QtWidgets.QStackedLayout()
        self.setMainLayout(self.taskLayout)

        backgroundWidget.setLayout(sideMenuLayout)
        layout.addLayout(self.taskLayout)

        self.setSideMenu(sideMenuLayout)
        sideMenuLayout.addStretch(0)

        self.setMainLayout(self.taskLayout)

        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(layout)

        self.setCentralWidget(mainWidget)

    def setSideMenu(self, layout):
        self.todayButton = QtWidgets.QPushButton("Project Base")
        self.nextWeekButton = QtWidgets.QPushButton("Task list")
        self.calendarButton = QtWidgets.QPushButton("Calendar")
        sideMenuButtons = [self.todayButton, self.nextWeekButton, self.calendarButton]
        for button in sideMenuButtons:
            button.setObjectName("sideMenuButton")
            layout.addWidget(button)
        # Выставление иконок бокового меню
        """
        sideMenuButtons[0].setIcon(QtGui.QIcon("today icon.png"))
        sideMenuButtons[1].setIcon(QtGui.QIcon("week icon.png"))
        sideMenuButtons[2].setIcon(QtGui.QIcon("calendar icon.png"))
        """
        sideMenuButtons[0].pressed.connect(self.ProjectBaseButtonPress)
        sideMenuButtons[1].pressed.connect(self.nextWeekButtonPress)
        sideMenuButtons[2].pressed.connect(self.calendarButtonPress)

    def setMainLayout(self, layout):
        today = self.ProjectBaseWidget()
        next_week = self.nextWeekWidget()
        calendar_widget = self.calendarWidget()
        # if
        layout.addWidget(today)
        layout.addWidget(next_week)
        #layout.addWidget(calendar_widget)
        self.labels = ["button1", "button2", "button3", "button4", "Button5"]
        for today_events in self.labels:
            label = QtWidgets.QLabel(today_events)
            layout.addWidget(label)

    def ProjectBaseWidget(self):
        widget = QtWidgets.QWidget(self)
        """
        month = date.today().month
        day = date.today().day
        today = f"{months[month - 1]}{day}"
        """
        #Label property
        self.project_base = QtWidgets.QLabel("Project base")
        self.project_base.setObjectName("project_base_label")
        self.project_base.setAlignment(QtCore.Qt.AlignCenter)

        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.tableWidget = QtWidgets.QTableWidget(self.page)
        self.tableWidget.setGeometry(QtCore.QRect(280, 80, 651, 641))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.addTodoEventButton = QtWidgets.QPushButton()
        #self.addTodoEventButton.setLocale()
        self.addTodoEventButton.setObjectName("addTodoEventButton")
        self.addTodoEventButton.setIcon(QtGui.QIcon("add event button.png"))
        self.addTodoEventButton.setToolTip("Add To Do Event")

        """
        layout.addWidget(self.project_base)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addTodoEventButton)
        layout.addStretch(0)
        """
        return widget

    def nextWeekWidget(self):
        widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout(widget)

        self.today_label = QtWidgets.QLabel("nextdfkv;xcv;xcToday")
        self.today_label.setObjectName("next_label")
        layout.addWidget(self.today_label)
        # setup layout for next week's widget
        return widget

    def calendarWidget(self):
        widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout(widget)
        # setup layout for calendar widget
        return widget

    def addTodoEvent(self):
        pass

    def ProjectBaseButtonPress(self):
        print("today button pressed")
        self.taskLayout.setCurrentIndex(0)

    def nextWeekButtonPress(self):
        print("Next week button pressed")
        self.taskLayout.setCurrentIndex(1)

    def calendarButtonPress(self):
        print("calendar button pressed")
        self.taskLayout.setCurrentIndex(2)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    app.exec_()
