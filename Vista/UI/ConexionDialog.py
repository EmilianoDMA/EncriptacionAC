# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConexionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConexionDialog(object):
    def setupUi(self, ConexionDialog):
        ConexionDialog.setObjectName("ConexionDialog")
        ConexionDialog.resize(342, 154)
        self.botones = QtWidgets.QDialogButtonBox(ConexionDialog)
        self.botones.setGeometry(QtCore.QRect(20, 120, 301, 21))
        self.botones.setOrientation(QtCore.Qt.Horizontal)
        self.botones.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.botones.setObjectName("botones")
        self.conexion_label = QtWidgets.QLabel(ConexionDialog)
        self.conexion_label.setGeometry(QtCore.QRect(140, 10, 68, 19))
        self.conexion_label.setAlignment(QtCore.Qt.AlignCenter)
        self.conexion_label.setObjectName("conexion_label")
        self.caja = QtWidgets.QFrame(ConexionDialog)
        self.caja.setGeometry(QtCore.QRect(9, 39, 321, 71))
        self.caja.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.caja.setFrameShadow(QtWidgets.QFrame.Raised)
        self.caja.setObjectName("caja")
        self.ip_label = QtWidgets.QLabel(self.caja)
        self.ip_label.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.ip_label.setObjectName("ip_label")
        self.ip = QtWidgets.QLineEdit(self.caja)
        self.ip.setGeometry(QtCore.QRect(150, 10, 151, 21))
        self.ip.setObjectName("ip")

        self.retranslateUi(ConexionDialog)
        self.botones.accepted.connect(ConexionDialog.accept)
        self.botones.rejected.connect(ConexionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConexionDialog)

    def retranslateUi(self, ConexionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConexionDialog.setWindowTitle(_translate("ConexionDialog", "Dialog"))
        self.conexion_label.setText(_translate("ConexionDialog", "Conexión"))
        self.ip_label.setText(_translate("ConexionDialog", "Dirección IP: "))

