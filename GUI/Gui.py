import functools
from GUI.WindowProjectAdd import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from Controllers.dbController import *


class Ui_MainWindo(object):
    style = "font-family: 'Segoe UI', sans-serif; font-size: 21px; font-style: bold;"
    db = dbController()
    connection = db.create_connection()
    cursor = connection.cursor()

    def setupUi(self, MainWindo):
        # Главное окно
        MainWindo.setObjectName("MainWindo")
        MainWindo.resize(1520, 600)#1300

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
        self.side_menu.setMinimumSize(QtCore.QSize(170, 0))
        self.gridLayout_3.addWidget(self.side_menu, 0, 0, 1, 1)
        # self.horizontalLayout_4.addWidget(self.side_menu)

        # self.side_menu.resize(self.side_menu.sizeHint())
        # Кнопки бокового меню
            # Кнопка таблицы с проектом
        self.ProjectBaseButton = QtWidgets.QPushButton(self.side_menu)
        self.ProjectBaseButton.setGeometry(QtCore.QRect(0, 0, 170, 30))
        self.ProjectBaseButton.pressed.connect(self.ProjectBaseButtonPress)  # Кнопка перехода на таблицу
        self.ProjectBaseButton.setText("Список проектов")
        self.ProjectBaseButton.setStyleSheet(self.style + "border: none;")
            # Кнопка страницы с задачами
        self.TasksButton = QtWidgets.QPushButton(self.side_menu)
        self.TasksButton.setGeometry(QtCore.QRect(0, 50, 130, 30))
        self.TasksButton.pressed.connect(self.SecondButton)

            # Кнопка страницы с настройками
        self.SettingsButton = QtWidgets.QPushButton(self.side_menu)
        self.SettingsButton.setGeometry(QtCore.QRect(0, 100, 170, 30))
        self.SettingsButton.pressed.connect(self.SettingsButtonPress)
        self.SettingsButton.setText("Настройки")
        self.SettingsButton.setStyleSheet(self.style + "border: none;")

        # Список страниц
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        # self.stackedWidget.setGeometry(QtCore.QRect(150, 0, 1250, 850))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setMinimumSize(QtCore.QSize(1321, 660))#980

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
        self.settings = self.settings_page()
        self.stackedWidget.addWidget(self.settings)

        self.updateTable(False)

        # Удаление ссылок из кнопки таблицы
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

    """
        mode - переменная отвечающая за режимы обновления таблицы. 
        True/False - с/без переопределением кнопок 
    """
    def updateTable(self, mode, added = 1, list=None):
        connection = self.db.create_connection()

        self.tableWidget.clear();
        self.tableWidget.setHorizontalHeaderLabels(
            ["Имя проекта", "Состояние", "Платформа", "Версия", "Ссылка на github", "",""])
        if not list:
            list = self.db.get_project()

        if mode:
            for i in range(len(self.stackedWidget), (len(self.stackedWidget) - len(list) + added), -1):
                widget = self.stackedWidget.widget(i - 1)
                self.stackedWidget.removeWidget(widget)
                # widget.deleteLater()
        self.tableWidget.setRowCount(len(list))
        print(list)
        for i in range(len(list)):
            # +2 Для кнопки редактирования и удаления
            for j in range(1, len(list[i])+2):
                if j == 2:
                    if list[i][j] is not None:
                        self.tableWidget.setItem(i, j - 1,
                                                 QTableWidgetItem(self.db.get_state(state_id=list[i][j])[0][1]))
                    else:
                        self.tableWidget.setItem(i, j - 1, QTableWidgetItem(f"{list[i][j]}"))
                if j == 3:
                    self.tableWidget.setItem(i, j - 1,
                                             QTableWidgetItem(self.db.get_platform(platform_id=list[i][j])[0][1]))
                if j == 1 or j == 4:
                    self.tableWidget.setItem(i, j - 1, QTableWidgetItem(f"{list[i][j]}"))
                if j == 5:
                    btn = QPushButton(f"{list[i][j].split('/')[len(list[i][j].split('/')) - 1]}")
                    btn.pressed.connect(functools.partial(self.gitButtonPress, i))
                    self.stackedWidget.addWidget(self.GitWebPage(list[i][j]))
                    self.tableWidget.setCellWidget(i, j - 1, btn)
                if j == 6 or j == 7:
                    btn = QPushButton()
                    if j == 6:
                        btn.setIcon(QIcon('Resources/edit.png'))
                    else:
                        btn.setIcon(QIcon('Resources/delete.png'))
                    btn.setMaximumSize(QtCore.QSize(50, 16777215))
                    btn.setStyleSheet("border: none;")
                    if j == 6:
                        pass
                        # btn.pressed.connect(functools.partial(self.gitButtonPress, i))
                    else:
                        btn.pressed.connect(functools.partial(self.delete_project_button_press, list[i][0]))
                    self.tableWidget.setCellWidget(i, j-1, btn)

        self.tableWidget.update();
        connection.close()

    def update_main_page(self):
        self.project_base_page.update()

    def settings_page(self):
        page = QtWidgets.QWidget()
        page.setObjectName("page_2")
        self.settingsLayout = QtWidgets.QWidget(page)
        self.settingsLayout.setGeometry(QtCore.QRect(0, 0, 1321, 641))
        self.settingsLayout.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.settingsLayout)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)

        self.stateLabel = QtWidgets.QLabel(self.settingsLayout)
        self.stateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.stateLabel.setWordWrap(False)
        self.stateLabel.setObjectName("label")
        self.stateLabel.setStyleSheet(self.style)
        self.stateLabel.setText("Список возможных состояний проекта")
        self.gridLayout.addWidget(self.stateLabel, 1, 0, 1, 1)
        self.stateEditButton = QtWidgets.QPushButton(self.settingsLayout)
        self.stateEditButton.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.stateEditButton, 1, 1, 1, 1)
        self.stateEditButton.setText("PushButton")

        self.label_2 = QtWidgets.QLabel(self.settingsLayout)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(self.style)
        self.label_2.setText("Платформы")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.platformEditBtn = QtWidgets.QPushButton(self.settingsLayout)
        self.platformEditBtn.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.platformEditBtn, 3, 1, 1, 1)
        self.platformEditBtn.setText("PushButton")

        self.pushButton_8 = QtWidgets.QPushButton(self.settingsLayout)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.settingsLayout)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setStyleSheet(self.style)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 2, 1, 1)
        #MainWindo.setCentralWidget(self.centralwidget)
        self.pushButton_8.setText("PushButton")
        self.label_3.setText("Добавить отдел")
        return page

    def ProjectBasePage(self):
        page = QtWidgets.QWidget()
        page.setObjectName("page")
        self.tableWidget = QtWidgets.QTableWidget(page)
        self.tableWidget.setGeometry(QtCore.QRect(280, 10, 1041, 650))
        self.tableWidget.setObjectName("tableWidget")

        # Создание полей таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(0, 280)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 240)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 50)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(4)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(6)

        self.sortLabel = QtWidgets.QLabel(page)
        self.sortLabel.setGeometry(QtCore.QRect(15, 10, 256, 50))
        self.sortLabel.setText("Сортировать таблицу по")
        self.sortLabel.setStyleSheet(self.style)
        self.sortMenu = QtWidgets.QComboBox(page)
        self.sortMenu.setGeometry(QtCore.QRect(10, 60, 256, 50))
        self.sortMenu.setObjectName("textBrowser")
        self.sortMenu.setStyleSheet(self.style)
        self.sortMenu.addItems(["Нет", "Имени", "Состоянию", "Платформе"])
        self.sortMenu.currentTextChanged.connect(self.update_main_page)

        self.sortButton = QtWidgets.QPushButton(page)
        self.sortButton.setGeometry(QtCore.QRect(60, 120, 150, 40))
        self.sortButton.setObjectName("sortButton")
        self.sortButton.setText("Сортировать")
        self.sortButton.setStyleSheet(self.style)
        self.sortButton.pressed.connect(self.sort_button_press)

        self.searchLabel = QtWidgets.QLabel(page)
        self.searchLabel.setGeometry(QtCore.QRect(80, 180, 256, 50))
        self.searchLabel.setText("Искать по")
        self.searchLabel.setStyleSheet(self.style)

        self.searchMenu = QtWidgets.QComboBox(page)
        self.searchMenu.setGeometry(QtCore.QRect(10, 240, 256, 50))
        self.searchMenu.setObjectName("textBrowser")
        self.searchMenu.setStyleSheet(self.style)
        self.searchMenu.addItems(["Нет", "Имени", "Состоянию", "Платформе"])
        self.searchMenu.currentTextChanged.connect(self.search_menu_selected)

        self.searchField = QtWidgets.QPlainTextEdit(page)
        self.searchField.setGeometry(QtCore.QRect(10, 300, 256, 41))
        self.searchField.setStyleSheet(self.style)
        self.searchField.setVisible(False)

        self.searchMenu2 = QtWidgets.QComboBox(page)
        self.searchMenu2.setGeometry(QtCore.QRect(10, 300, 256, 41))
        self.searchMenu2.setStyleSheet(self.style)
        self.searchMenu2.setVisible(False)

        self.searchButton = QtWidgets.QPushButton(page)
        self.searchButton.setGeometry(QtCore.QRect(60, 360, 150, 40))
        self.searchButton.setStyleSheet(self.style)
        self.searchButton.setText("Искать")
        self.searchButton.setVisible(False)
        self.searchButton.pressed.connect(self.search_button_pressed)

        self.addButton = QtWidgets.QPushButton(page)
        self.addButton.setGeometry(QtCore.QRect(60, 600, 150, 40))
        self.addButton.setObjectName("pushButton_2")
        self.addButton.setStyleSheet(self.style)
        self.addButton.setText("Добавить")
        return page

    def GitWebPage(self, url):
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

    """Блок обработчиков кнопок"""
    def sort_button_press(self):
        connection = self.db.create_connection()
        if self.sortMenu.currentText() == "Нет":
            self.updateTable(True, 0)
        if self.sortMenu.currentText() == "Имени":
            self.updateTable(True, 0, self.db.get_project(*["project_name", "project_id"]))
        if self.sortMenu.currentText() == "Состоянию":
            self.updateTable(True, 0, self.db.get_project(*["state_id", "project_id"]))
        if self.sortMenu.currentText() == "Платформе":
            self.updateTable(True, 0, self.db.get_project(*["platform_id", "project_id"]))
        connection.close()
            # if list:
            #     list = self.db.get_project(["platform_id", "project_id"])
            # else:
            #     list = self.db.get_project()

    def search_menu_selected(self):
        if self.searchMenu.currentText() == "Нет":
            self.updateTable(True, 0)
            self.searchField.setVisible(False)
            self.searchMenu2.setVisible(False)
            self.searchButton.setVisible(False)
        if self.searchMenu.currentText() == "Имени":
            self.searchField.setVisible(True)
            self.searchMenu2.setVisible(False)
            self.searchButton.setVisible(True)
        if self.searchMenu.currentText() == "Состоянию":
            connection = self.db.create_connection()
            self.searchField.setVisible(False)
            self.searchMenu2.setVisible(True)
            self.searchButton.setVisible(True)
            self.searchMenu2.clear()
            list = self.db.get_state()
            buf = ['Нет']
            for i in list:
                buf.append(i[1])
            self.searchMenu2.addItems(buf)
            connection.close()
        if self.searchMenu.currentText() == "Платформе":
            connection = self.db.create_connection()
            self.searchField.setVisible(False)
            self.searchMenu2.setVisible(True)
            self.searchButton.setVisible(True)
            self.searchMenu2.clear()
            list = self.db.get_platform()
            buf = ['Нет']
            for i in list:
                buf.append(i[1])
            self.searchMenu2.addItems(buf)
            connection.close()

    def search_button_pressed(self):
        connection = self.db.create_connection()
        if self.searchMenu2.currentText() == "Нет":
            self.updateTable(True, 0)
            return
        if self.searchMenu.currentText() == "Имени":
            list = self.db.project_search(project_name = self.searchField.toPlainText())
            self.updateTable(True, 0, list)
        if self.searchMenu.currentText() == "Состоянию":
            list = self.db.project_search(
                state_id=self.db.get_state(state=self.searchMenu2.currentText())[0][0])
            self.updateTable(True, 0, list)
        if self.searchMenu.currentText() == "Платформе":
            list = self.db.project_search(
                platform_id = self.db.get_platform(platform = self.searchMenu2.currentText())[0][0])
            self.updateTable(True, 0, list)
        connection.close()

    def delete_project_button_press(self, primary_key):
        connection = self.db.create_connection()
        self.db.delete_project(primary_key)
        connection.close()
        self.updateTable(True)

    def SettingsButtonPress(self):
        self.stackedWidget.setCurrentIndex(2)
        self.ProjectBaseButton.setStyleSheet(self.style + "color: rgb(0, 0, 0);" + "border: none;")
        self.SettingsButton.setStyleSheet(self.style + "color: rgb(0, 0, 0);" + "border: none;")
        self.side_menu.setStyleSheet("background-color: lightgrey")
        self.centralwidget.setStyleSheet("background-color: midlight")
        print("SettingsButtonPress")

    def gitButtonPress(self, index):
        self.centralwidget.setStyleSheet("background-color: #24292f")
        self.side_menu.setStyleSheet("background-color: #24292f")
        self.ProjectBaseButton.setStyleSheet(self.style + "color: rgb(255, 255, 255);" + "border: none;")
        self.SettingsButton.setStyleSheet(self.style + "color: rgb(255, 255, 255);" + "border: none;")
        self.stackedWidget.setCurrentIndex(3 + index)
        print("gitButtonPress")

    def ProjectBaseButtonPress(self):
        self.stackedWidget.setCurrentIndex(0)
        self.side_menu.setStyleSheet("background-color: lightgrey")
        self.centralwidget.setStyleSheet("background-color: midlight")
        self.ProjectBaseButton.setStyleSheet(self.style + "color: rgb(0, 0, 0);" + "border: none;")
        self.SettingsButton.setStyleSheet(self.style + "color: rgb(0, 0, 0);" + "border: none;")
        print("ProjectBaseButtonPress")

    def SecondButton(self):
        self.stackedWidget.setCurrentIndex(1)
        print("SecondButton")

    def retranslateUi(self, MainWindo):
        _translate = QtCore.QCoreApplication.translate
        MainWindo.setWindowTitle(_translate("MainWindo", "Game Dev Company databases"))
