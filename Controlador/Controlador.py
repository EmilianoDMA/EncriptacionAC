from Modelo import Modelo

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = Modelo.Modelo(self)

    def conectar(self, ip, puerto):
        self.modelo.conectar(ip, puerto)

    def recibirMensaje(self, mensaje):
        print("LLEGO AL CONTROLADOOOOOOOOR")
        pass
        #self.vista.escribirMensajeRecibido(mensaje)

    def enviarMensaje(self):
        mensaje = self.vista.getContenidoMensaje()
        self.modelo.enviarMensaje(mensaje)
        self.vista.escribirMensajeEnviado(mensaje)

    def desconectar(self):
        self.modelo.desconectar()
