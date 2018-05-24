from PyQt5 import QtWidgets
from Vista.UI import Ventana, ConexionDialog
from Controlador.Controlador import Controlador

class Vista(QtWidgets.QMainWindow):
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

    def deshabilitarVista(self):
        self.ventana.escribir.setReadOnly(True)
        self.ventana.enviar.setEnabled(False)

    def habilitarVista(self):
        self.ventana.escribir.setReadOnly(False)
        self.ventana.enviar.setEnabled(True)

    def getContenidoMensaje(self):
        mensaje = self.ventana.escribir.toPlainText()
        self.ventana.escribir.clear()
        return mensaje

    def escribirMensajeRecibido(self, mensaje):
        contenido = self.ventana.mensajes.toPlainText()
        self.ventana.mensajes.clear()
        self.ventana.mensajes.setPlainText(contenido+">>>"+mensaje+"\n")

    def escribirMensajeEnviado(self, mensaje):
        contenido = self.ventana.mensajes.toPlainText()
        self.ventana.mensajes.clear()
        self.ventana.mensajes.setPlainText(contenido+">"+mensaje+"\n")

    def enviarMensaje(self):
        self.ventana.escribir.cut()
        self.controlador.enviarMensaje()

    def cerrarConexiones(self):
        self.controlador.desconectar()

    def conectar(self, ip, puerto):
        self.controlador.conectar(ip, puerto)
        self.habilitarVista()
