import functools
import sys

import GUI.WindowProjectAdd
from GUI.WindowProjectAdd import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from dbController import *

class Ui_MainWindo(object):
    db = dbController()
    connection = db.create_connection()
    cursor = connection.cursor()

    def setupUi(self, MainWindo):
        # Главное окно
        MainWindo.setObjectName("MainWindo")
        MainWindo.resize(1400, 900)

        MainWindo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.centralwidget = QtWidgets.QWidget(MainWindo)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setEnabled(True)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        MainWindo.setCentralWidget(self.centralwidget)

        # Боковое меню
        self.side_menu = QtWidgets.QFrame(self.centralwidget)
        self.side_menu.setGeometry(QtCore.QRect(0, 0, 150, 850))
        self.side_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_menu.setStyleSheet("background-color: lightgrey")
        self.side_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_menu.setObjectName("side_menu")
        self.side_menu.setMinimumSize(QtCore.QSize(150, 0))
        self.gridLayout_3.addWidget(self.side_menu, 0, 0, 1, 1)
        #self.horizontalLayout_4.addWidget(self.side_menu)

        #self.side_menu.resize(self.side_menu.sizeHint())
        # Кнопки бокового меню
            # Кнопка таблицы с проектом
        self.ProjectBaseButton = QtWidgets.QPushButton(self.side_menu)
        self.ProjectBaseButton.setGeometry(QtCore.QRect(0, 0, 130, 30))
        self.ProjectBaseButton.pressed.connect(self.ProjectBaseButtonPress)  # Кнопка перехода на таблицу
            # Кнопка страницы с задачами
        self.TasksButton = QtWidgets.QPushButton(self.side_menu)
        self.TasksButton.setGeometry(QtCore.QRect(0, 50, 130, 30))
        self.TasksButton.pressed.connect(self.SecondButton)
            # Кнопка страницы с настройками
        self.SettingsButton = QtWidgets.QPushButton(self.side_menu)
        self.SettingsButton.setGeometry(QtCore.QRect(0, 100, 130, 30))
        self.SettingsButton.pressed.connect(self.SettingsButtonPress)


        #Список страниц
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(150, 0, 1250, 850))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setMinimumSize(QtCore.QSize(980, 800))

        # Страница с таблицей базы
        self.project_base_page = self.ProjectBasePage()
        self.stackedWidget.addWidget(self.project_base_page)

        # Страница тасков
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.taskbtn = QtWidgets.QPushButton("Task_button", self.page_2)
        self.taskbtn.setGeometry(QtCore.QRect(90, 160, 93, 28))
        self.taskbtn.setObjectName("task_page")
        self.stackedWidget.addWidget(self.page_2)

        # Страница с настройками
        self.settings = self.settingsPage()
        self.stackedWidget.addWidget(self.settings)

        self.updateTable()

        #Удаление ссылок из кнопки таблицы
        """for i in range(len(self.stackedWidget),(len(self.stackedWidget)-len(list)),-1):
            widget = self.stackedWidget.widget(i-1)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()"""


        MainWindo.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindo)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindo.setMenuBar(self.menubar)

        self.retranslateUi(MainWindo)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindo)
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 1, 1, 1)

    def updateTable(self):
        connection = self.db.create_connection()

        self.tableWidget.clear();
        self.tableWidget.setHorizontalHeaderLabels(
            ["Имя проекта", "Состояние", "Платформа", "Версия", "Ссылка на github"])
        list = self.db.get_project_list()
        self.tableWidget.setRowCount(len(list))
        print(list)
        for i in range(len(list)):
            for j in range(1, len(list[i])):
                if j == 2:
                    if list[i][j] != None:
                        self.tableWidget.setItem(i, j - 1,
                                                QTableWidgetItem(self.db.get_state(state_id=list[i][j])[0][1]))
                    else:
                        self.tableWidget.setItem(i, j - 1, QTableWidgetItem(f"{list[i][j]}"))
                if j == 3:
                    self.tableWidget.setItem(i, j - 1,
                                             QTableWidgetItem(self.db.get_platform(platform_id=list[i][j])[0][1]))
                if j != 5 and j != 3 and j != 2:
                    self.tableWidget.setItem(i, j - 1, QTableWidgetItem(f"{list[i][j]}"))
                if j == 5:
                    btn = QPushButton(f"{list[i][j].split('/')[len(list[i][j].split('/')) - 1]}")
                    btn.pressed.connect(functools.partial(self.gitButtonPress, i))
                    self.stackedWidget.addWidget(self.GitWebPage(list[i][j]))
                    self.tableWidget.setCellWidget(i, j - 1, btn)
        self.tableWidget.update();
        connection.close()

    def settingsPage(self):
        page = QtWidgets.QWidget()
        page.setObjectName("settings")
        return page

    def ProjectBasePage(self):
        page = QtWidgets.QWidget()
        page.setObjectName("page")
        self.tableWidget = QtWidgets.QTableWidget(page)
        self.tableWidget.setGeometry(QtCore.QRect(440, 80, 762, 641))
        self.tableWidget.setObjectName("tableWidget")

        # Создание полей таблицы
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setColumnWidth(4, 241)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4)

        self.textBrowser = QtWidgets.QTextBrowser(page)
        self.textBrowser.setGeometry(QtCore.QRect(10, 80, 256, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(page)
        self.pushButton.setGeometry(QtCore.QRect(90, 160, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(page)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 760, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        return page

    def GitWebPage(self,url):
        page = QtWidgets.QWidget()
        LayoutGit = QtWidgets.QGridLayout(page)
        LayoutGit.setObjectName("gridLayout_3")
        page.setObjectName("page_3")
        page.setStyleSheet("background-color: #24292f")
        web = QWebEngineView(page)
        web.setGeometry(QtCore.QRect(0, 0, 1250, 850))
        web.sizePolicy().horizontalPolicy()
        web.load(QUrl(url))
        web.show()
        LayoutGit.addWidget(web)
        return page


    """def openProjectAddWindow(self):
        dialog = ClssDialog(self)
        dialog.exec_()"""


    """Блок обработчиков кнопок"""
    def SettingsButtonPress(self):
        self.stackedWidget.setCurrentIndex(2)
        print("SettingsButtonPress")

    def gitButtonPress(self,index):
        self.centralwidget.setStyleSheet("background-color: #24292f")
        self.side_menu.setStyleSheet("background-color: #24292f")
        self.stackedWidget.setCurrentIndex(3+index)
        print("gitButtonPress")

    def ProjectBaseButtonPress(self):
        self.stackedWidget.setCurrentIndex(0)
        self.side_menu.setStyleSheet("background-color: lightgrey")
        self.centralwidget.setStyleSheet("background-color: midlight")
        print("ProjectBaseButtonPress")

    def SecondButton(self):
        self.stackedWidget.setCurrentIndex(1)
        print("SecondButton")

    def retranslateUi(self, MainWindo):
        _translate = QtCore.QCoreApplication.translate
        MainWindo.setWindowTitle(_translate("MainWindo", "Game Dev Company databases"))
        self.pushButton.setText(_translate("MainWindo", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindo", "PushButton"))
