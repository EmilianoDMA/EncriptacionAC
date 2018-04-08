from Modelo import Modelo

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = Modelo.Modelo(self)

    def conectar(self, ip, puerto):
        pass

    def recibirMensaje(self, mensaje):
        self.vista.escribirMensajeRecibido(mensaje)

    def enviarMensaje(self):
        self.vista.escribirMensajeEnviado()

    def desconectar(self):
        pass
