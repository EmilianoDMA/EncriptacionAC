from PyQt5 import QtWidgets
from Vista.UI import ConexionDialog
from Controlador.Controlador import Controlador

class DialogoConexion(QtWidgets.QDialog):
    def __init__(self, Ventana):
        super().__init__()
        self.ventana = Ventana
        self.dialogo = ConexionDialog.Ui_ConexionDialog()
        self.dialogo.setupUi(self)
        self.initDialogo()
        self.show()

    def initDialogo(self):
        self.ventana.deshabilitarVista()
        self.dialogo.botones.accepted.connect(self.conectar)
        self.dialogo.botones.rejected.connect(self.desconectar)

    def conectar(self):
        ip = self.dialogo.ip.text()
        puerto = int(self.dialogo.puerto.text())
        self.ventana.conectar(ip, puerto)

    def desconectar(self):
        self.ventana.close()
