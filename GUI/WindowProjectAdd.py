from GUI.Gui import *
from Controllers.dbController import *
from PyQt5 import QtWidgets, QtCore

class WindowProjectAdd(QtWidgets.QDialog):
    style = "font-family: 'Segoe UI', sans-serif; font-size: 21px; font-style: bold;"
    db = dbController()

    def __init__(self, parent=None):
        super(WindowProjectAdd, self).__init__(parent)
        _translate = QtCore.QCoreApplication.translate
        self.setFixedSize(500, 310)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowTitle(_translate("MainWindow", "Добавить проект"))
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)

        # Имя проекта
        self.projectName = QtWidgets.QLabel(self.centralwidget)
        self.projectName.setStyleSheet(self.style)
        self.projectName.setObjectName("label")
        self.gridLayout.addWidget(self.projectName, 0, 0, 1, 1)
        self.projectName.setText(_translate("MainWindow", "Имя проекта*"))

        self.setProjectName = QtWidgets.QTextEdit(self.centralwidget)
        self.setProjectName.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setProjectName.setObjectName("setProjectName")
        self.gridLayout.addWidget(self.setProjectName, 0, 1, 1, 1)

        # Платформа
        self.platform = QtWidgets.QLabel(self.centralwidget)
        self.platform.setStyleSheet(self.style)
        self.platform.setObjectName("label_4")
        self.gridLayout.addWidget(self.platform, 4, 0, 1, 1)
        self.platform.setText(_translate("MainWindow", "Платформа*"))

        # Поле платформы
        self.setPlatform = QtWidgets.QComboBox(self.centralwidget)
        self.setPlatform.setMinimumSize(QtCore.QSize(310, 30))
        self.setPlatform.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setPlatform.setObjectName("setPlatform")
        self.setPlatform.clear()
        connection = self.db.create_connection()
        list = self.db.get_platform()
        platform_list = []
        platform_list.append('None')
        for i in list:
            platform_list.append(i[1])
        self.setPlatform.addItems(platform_list)
        self.gridLayout.addWidget(self.setPlatform, 4, 1, 1, 1)
        connection.close()

        # Поле состояния
        self.state = QtWidgets.QLabel(self.centralwidget)
        self.state.setStyleSheet(self.style)
        self.state.setObjectName("state")
        self.gridLayout.addWidget(self.state, 2, 0, 1, 1)
        self.state.setText(_translate("MainWindow", "Состояние"))
        self.setState = QtWidgets.QComboBox(self.centralwidget)
        self.setState.setMinimumSize(QtCore.QSize(0, 30))
        self.setState.setObjectName("setState")
        list.clear()
        connection = self.db.create_connection()
        list = self.db.get_state()
        state_list = []
        state_list.append('None')
        for i in list:
            state_list.append(i[1])
        self.setState.addItems(state_list)
        self.gridLayout.addWidget(self.setState, 2, 1, 1, 1)
        connection.close()

        # Указатель на обязательные поля
        self.notion = QtWidgets.QLabel(self.centralwidget)
        self.notion.setObjectName("label_3")
        self.gridLayout.addWidget(self.notion, 10, 1, 1, 1)
        self.notion.setText(_translate("MainWindow", "*Обязательные поля"))

        # Поле ссылки на github
        self.gitUrl = QtWidgets.QLabel(self.centralwidget)
        self.gitUrl.setStyleSheet(self.style)
        self.gitUrl.setObjectName("gitUrl")
        self.gridLayout.addWidget(self.gitUrl, 6, 0, 1, 1)
        self.gitUrl.setText(_translate("MainWindow", "Ссылка на GitHub"))
        self.setGitUrl = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.setGitUrl.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setGitUrl.setObjectName("setGitUrl")
        self.gridLayout.addWidget(self.setGitUrl, 6, 1, 1, 1)

        self.version = QtWidgets.QLabel(self.centralwidget)
        self.version.setStyleSheet(self.style)
        self.version.setObjectName("label_6")
        self.gridLayout.addWidget(self.version, 5, 0, 1, 1)
        self.version.setText(_translate("MainWindow", "Версия"))
        self.setVersion = QtWidgets.QTextEdit(self.centralwidget)
        self.setVersion.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setVersion.setObjectName("textEdit_3")
        self.gridLayout.addWidget(self.setVersion, 5, 1, 1, 1)

        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setObjectName("addBtn")
        self.gridLayout.addWidget(self.addBtn, 9, 1, 1, 1)
        self.addBtn.setText(_translate("MainWindow", "Добавить проект"))
        self.addBtn.pressed.connect(self.btnAdd)

        self.CancelBtn = QtWidgets.QPushButton(self.centralwidget)
        self.CancelBtn.setObjectName("CancelBtn")
        self.gridLayout.addWidget(self.CancelBtn, 9, 0, 1, 1)
        self.CancelBtn.setText(_translate("MainWindow", "Отмена"))
        self.CancelBtn.pressed.connect(self.btnClose)

    def btnAdd(self):
        req = {}
        name = self.setProjectName.toPlainText()
        platf = self.setPlatform.currentText()
        state = self.setState.currentText()
        giturl = self.setGitUrl.toPlainText()
        vers = self.setVersion.toPlainText()
        if platf == 'None':
            print('Error')
        if name == '':
            print('Error')
        if vers != '':
            req['project_version'] = vers
        if state != 'None':
            req['state_id'] = state
        if giturl != '':
            req['github_url'] = giturl
        connection = self.db.create_connection()
        self.db.add_project(name, platf, **req)
        connection.close()
        self.close()
        self.deleteLater()

    def btnClose(self):
        self.close()
        self.deleteLater()
