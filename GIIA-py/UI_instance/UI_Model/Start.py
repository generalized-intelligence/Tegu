# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_start(object):
    def setupUi(self, start):
        start.setObjectName("start")
        start.resize(964, 718)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(start.sizePolicy().hasHeightForWidth())
        start.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(start)
        self.verticalLayout.setObjectName("verticalLayout")
        self.boxFile = QtWidgets.QGroupBox(start)
        self.boxFile.setObjectName("boxFile")
        self.button_new = QtWidgets.QPushButton(self.boxFile)
        self.button_new.setGeometry(QtCore.QRect(120, 80, 131, 61))
        self.button_new.setObjectName("button_new")
        self.button_open = QtWidgets.QPushButton(self.boxFile)
        self.button_open.setGeometry(QtCore.QRect(420, 80, 131, 61))
        self.button_open.setObjectName("button_open")
        self.button_pack = QtWidgets.QPushButton(self.boxFile)
        self.button_pack.setGeometry(QtCore.QRect(730, 80, 131, 61))
        self.button_pack.setObjectName("button_pack")
        self.verticalLayout.addWidget(self.boxFile)
        self.listRecent = QtWidgets.QListView(start)
        self.listRecent.setObjectName("listRecent")
        self.verticalLayout.addWidget(self.listRecent)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)

        self.retranslateUi(start)
        QtCore.QMetaObject.connectSlotsByName(start)

    def retranslateUi(self, start):
        _translate = QtCore.QCoreApplication.translate
        start.setWindowTitle(_translate("start", "Form"))
        self.boxFile.setTitle(_translate("start", "新项目"))
        self.button_new.setText(_translate("start", "新建项目"))
        self.button_open.setText(_translate("start", "打开项目文件"))
        self.button_pack.setText(_translate("start", "打包"))


