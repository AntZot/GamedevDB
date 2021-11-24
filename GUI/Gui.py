import functools

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
        MainWindo.resize(1400, 850)
        print(type(MainWindo))
        MainWindo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.centralwidget = QtWidgets.QWidget(MainWindo)
        self.centralwidget.setObjectName("centralwidget")

        # Боковое меню
        self.side_menu = QtWidgets.QFrame(self.centralwidget)
        self.side_menu.setGeometry(QtCore.QRect(0, 0, 150, 850))
        self.side_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_menu.setStyleSheet("background-color: lightgrey")
        self.side_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_menu.setObjectName("side_menu")

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

        list = self.db.get_project_list()
        self.tableWidget.setRowCount(len(list))
        print(list)
        for i in range(len(list)):
            for j in range(1, len(list[i])):
                if j != 5:
                    self.tableWidget.setItem(i, j - 1, QTableWidgetItem(f"{list[i][j]}"))
                else:
                    btn = QPushButton(f"{list[i][j].split('/')[len(list[i][j].split('/')) - 1]}")
                    btn.pressed.connect(functools.partial(self.gitButtonPress,i))
                    self.stackedWidget.addWidget(self.GitWebPage(list[i][j]))
                    self.tableWidget.setCellWidget(i, j - 1, btn)

        #Удаление ссылок из кнопки таблицы
        """for i in range(len(self.stackedWidget),(len(self.stackedWidget)-len(list)),-1):
            widget = self.stackedWidget.widget(i-1)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()"""

        #self.stackedWidget.addWidget(self.GitWebPage("https://github.com/AntZot/GamedevDB")) #3 страница

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

    def settingsPage(self):
        page = QtWidgets.QWidget()
        page.setObjectName("settings")
        return page

    def ProjectBasePage(self):
        page = QtWidgets.QWidget()
        page.setObjectName("page")
        self.tableWidget = QtWidgets.QTableWidget(page)
        self.tableWidget.setGeometry(QtCore.QRect(440, 80, 1000, 641))
        self.tableWidget.setObjectName("tableWidget")

        # Создание полей таблицы
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setColumnWidth(4, 241)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4)
        self.tableWidget.setHorizontalHeaderLabels(["Имя проекта", "Состояние","Платформа","Версия","Ссылка на github"])

        self.textBrowser = QtWidgets.QTextBrowser(page)
        self.textBrowser.setGeometry(QtCore.QRect(10, 80, 256, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(page)
        self.pushButton.setGeometry(QtCore.QRect(90, 160, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(page)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 760, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.pressed.connect(self.gitButtonPress)
        return page

    def GitWebPage(self,url):
        page = QtWidgets.QWidget()

        self.return_back_btn = QtWidgets.QPushButton("Return back", self.side_menu)
        self.return_back_btn.setGeometry(QtCore.QRect(10, 750, 130, 40))
        self.return_back_btn.setObjectName("return_back_btn")
        self.return_back_btn.setStyleSheet("background-color: white; "
                                           "border-radius: 7px; "
                                           "font-family: 'Segoe UI', sans-serif; "
                                           "font-size: 21px; "
                                           "font-style: bold;")
        self.return_back_btn.pressed.connect(self.ProjectBaseButtonPress)
        self.return_back_btn.setVisible(False)
        page.setObjectName("page_3")
        page.setStyleSheet("background-color: #24292f")
        web = QWebEngineView(page)
        web.setGeometry(QtCore.QRect(0, 0, 1250, 850))
        web.sizePolicy().horizontalPolicy()
        web.load(QUrl(url))
        web.show()
        return page


    """Блок обработчиков кнопок"""
    def SettingsButtonPress(self):
        self.return_back_btn.setVisible(False)
        self.stackedWidget.setCurrentIndex(2)
        print("SettingsButtonPress")

    def gitButtonPress(self,index):
        self.side_menu.setStyleSheet("background-color: #24292f")
        self.return_back_btn.setVisible(True)
        self.stackedWidget.setCurrentIndex(3+index)
        print("gitButtonPress")

    def ProjectBaseButtonPress(self):
        self.stackedWidget.setCurrentIndex(0)
        self.return_back_btn.setVisible(False)
        self.side_menu.setStyleSheet("background-color: lightgrey")
        print("ProjectBaseButtonPress")

    def SecondButton(self):
        self.return_back_btn.setVisible(False)
        self.stackedWidget.setCurrentIndex(1)
        print("SecondButton")

    def retranslateUi(self, MainWindo):
        _translate = QtCore.QCoreApplication.translate
        MainWindo.setWindowTitle(_translate("MainWindo", "Game Dev Company databases"))
        self.pushButton.setText(_translate("MainWindo", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindo", "PushButton"))

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindo = QtWidgets.QMainWindow()
    ui = Ui_MainWindo()
    ui.setupUi(MainWindo)
    MainWindo.show()
    sys.exit(app.exec_())
