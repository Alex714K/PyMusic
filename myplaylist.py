# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myplaylist.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainPlaylist(object):
    def setupUi(self, MainPlaylist):
        MainPlaylist.setObjectName("MainPlaylist")
        MainPlaylist.resize(1137, 593)
        self.centralwidget = QtWidgets.QWidget(MainPlaylist)
        self.centralwidget.setObjectName("centralwidget")
        self.custom_button = QtWidgets.QPushButton(self.centralwidget)
        self.custom_button.setGeometry(QtCore.QRect(10, 510, 93, 28))
        self.custom_button.setObjectName("custom_button")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(6, 0, 1121, 501))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 100, -1, 100)
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.delete_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.up_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.up_button.setObjectName("up_button")
        self.verticalLayout.addWidget(self.up_button)
        self.down_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.down_button.setObjectName("down_button")
        self.verticalLayout.addWidget(self.down_button)
        self.edit_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.edit_button.setObjectName("edit_button")
        self.verticalLayout.addWidget(self.edit_button)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.queue = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.queue.setColumnCount(1)
        self.queue.setObjectName("queue")
        self.queue.setRowCount(0)
        self.horizontalLayout.addWidget(self.queue)
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(110, 514, 991, 20))
        self.name.setObjectName("name")
        MainPlaylist.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainPlaylist)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1137, 26))
        self.menubar.setObjectName("menubar")
        MainPlaylist.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainPlaylist)
        self.statusbar.setObjectName("statusbar")
        MainPlaylist.setStatusBar(self.statusbar)

        self.retranslateUi(MainPlaylist)
        QtCore.QMetaObject.connectSlotsByName(MainPlaylist)

    def retranslateUi(self, MainPlaylist):
        _translate = QtCore.QCoreApplication.translate
        MainPlaylist.setWindowTitle(_translate("MainPlaylist", "MainWindow"))
        self.custom_button.setText(_translate("MainPlaylist", "Add music"))
        self.add_button.setText(_translate("MainPlaylist", "Add"))
        self.delete_button.setText(_translate("MainPlaylist", "Delete"))
        self.up_button.setText(_translate("MainPlaylist", "Up"))
        self.down_button.setText(_translate("MainPlaylist", "Down"))
        self.edit_button.setText(_translate("MainPlaylist", "Edit"))
        self.name.setText(_translate("MainPlaylist", "Вставлен трек:  None"))
