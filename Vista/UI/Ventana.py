# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ventana.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(551, 411)
        self.principal = QtWidgets.QWidget(MainWindow)
        self.principal.setObjectName("principal")
        self.caja_mensajes = QtWidgets.QFrame(self.principal)
        self.caja_mensajes.setGeometry(QtCore.QRect(10, 10, 531, 301))
        self.caja_mensajes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.caja_mensajes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.caja_mensajes.setObjectName("caja_mensajes")
        self.scroll_mensajes = QtWidgets.QScrollArea(self.caja_mensajes)
        self.scroll_mensajes.setGeometry(QtCore.QRect(10, 10, 511, 281))
        self.scroll_mensajes.setWidgetResizable(True)
        self.scroll_mensajes.setObjectName("scroll_mensajes")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 509, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.mensajes = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.mensajes.setGeometry(QtCore.QRect(0, 0, 511, 281))
        self.mensajes.setObjectName("mensajes")
        self.scroll_mensajes.setWidget(self.scrollAreaWidgetContents)
        self.caja_escribir = QtWidgets.QFrame(self.principal)
        self.caja_escribir.setGeometry(QtCore.QRect(10, 320, 531, 81))
        self.caja_escribir.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.caja_escribir.setFrameShadow(QtWidgets.QFrame.Raised)
        self.caja_escribir.setObjectName("caja_escribir")
        self.scroll_escribir = QtWidgets.QScrollArea(self.caja_escribir)
        self.scroll_escribir.setGeometry(QtCore.QRect(10, 10, 451, 61))
        self.scroll_escribir.setWidgetResizable(True)
        self.scroll_escribir.setObjectName("scroll_escribir")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 449, 59))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.escribir = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.escribir.setGeometry(QtCore.QRect(0, 0, 451, 61))
        self.escribir.setObjectName("escribir")
        self.scroll_escribir.setWidget(self.scrollAreaWidgetContents_2)
        self.enviar = QtWidgets.QPushButton(self.caja_escribir)
        self.enviar.setGeometry(QtCore.QRect(470, 10, 51, 61))
        self.enviar.setText("")
        self.enviar.setObjectName("enviar")
        MainWindow.setCentralWidget(self.principal)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

