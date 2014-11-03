# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Nov  3 17:33:00 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(272, 101)
        Dialog.setMinimumSize(QtCore.QSize(272, 101))
        Dialog.setMaximumSize(QtCore.QSize(272, 101))
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 271, 101))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.toLanguageLabel = QtWidgets.QLabel(self.widget)
        self.toLanguageLabel.setObjectName("toLanguageLabel")
        self.gridLayout.addWidget(self.toLanguageLabel, 0, 0, 1, 1)
        self.fromLanguageLabel = QtWidgets.QLabel(self.widget)
        self.fromLanguageLabel.setObjectName("fromLanguageLabel")
        self.gridLayout.addWidget(self.fromLanguageLabel, 0, 1, 1, 1)
        self.fromLanguage = QtWidgets.QComboBox(self.widget)
        self.fromLanguage.setObjectName("fromLanguage")
        self.gridLayout.addWidget(self.fromLanguage, 1, 0, 1, 1)
        self.toLanguage = QtWidgets.QComboBox(self.widget)
        self.toLanguage.setObjectName("toLanguage")
        self.gridLayout.addWidget(self.toLanguage, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.toLanguageLabel.setText(_translate("Dialog", "From language"))
        self.fromLanguageLabel.setText(_translate("Dialog", "To language"))
        self.pushButton.setText(_translate("Dialog", "Record"))
        self.pushButton_2.setText(_translate("Dialog", "Say"))

