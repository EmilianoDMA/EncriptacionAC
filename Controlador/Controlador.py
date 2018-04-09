from Modelo import Modelo

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = Modelo.Modelo(self)

    def conectar(self, ip, puerto):
        pass

    def recibirMensaje(self, mensaje):
        self.vista.escribirMensajeRecibido(mensaje)

    def enviarMensaje(self, mensaje):
        self.vista.escribirMensajeEnviado(mensaje)

    def desconectar(self):
        pass
