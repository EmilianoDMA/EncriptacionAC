from PyQt5.QtWidgets import QMainWindow

from Vista.UI import Ventana
from Controlador.Controlador import Controlador

class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controlador = Controlador(self)
        self.ventana = Ventana.Ui_MainWindow()
        self.ventana.setupUi(self)
        self.inicializaUI()
        self.show()

    def inicializaUI(self):
        self.ventana.mensajes.setReadOnly(True)
        self.ventana.enviar.clicked.connect(self.controlador.enviarMensaje)

    def escribirMensajeRecibido(self, mensaje):
        self.ventana.mensajes.setText(mensaje)

    def escribirMensajeEnviado(self):
        self.ventana.mensajes.append("")
