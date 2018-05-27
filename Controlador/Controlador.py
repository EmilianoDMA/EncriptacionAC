from PyQt5 import QtCore
from Modelo import Modelo

class Controlador(QtCore.QObject):
    recibir_mensaje = QtCore.pyqtSignal(str)

    def __init__(self, vista):
        QtCore.QObject.__init__(self)
        self.vista = vista
        self.modelo = Modelo.Modelo(self)

    def conectar(self, ip, puerto):
        self.modelo.conectar(ip, puerto)

    def recibirMensaje(self, mensaje):
        self.recibir_mensaje.emit(mensaje)

    def enviarMensaje(self, mensaje):
        mensaje = self.vista.getContenidoMensaje()
        self.modelo.enviarMensaje(mensaje)
        self.vista.escribirMensajeEnviado(mensaje)

    def limpiarMensajes(self):
        self.vista.limpiarMensajes()

    def informarError(self, error):
        self.vista.informarError(error)

    def deshabilitarVista(self):
        self.vista.deshabilitarVista()

    def desconectar(self):
        self.modelo.desconectar()
