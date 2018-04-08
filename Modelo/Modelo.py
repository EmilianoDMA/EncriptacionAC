import sys
import random
import binascii
import socket
import threading
from pdb import set_trace


class Modelo():
    def __init__(self, controlador):
        self.controlador = controlador
        self.envio = None
        self.recep = None
        self.mensajes_recv = []
        self.mensajes_env = []

    def conectar(self, ip, puerto):
        # TODO Crear la conexion en su propio hilo
        self.envio = ConexionSaliente(ip, puerto)
        # TODO Crear la conexion en su propio hilo
        self.recep = ConexionEntrante(ip, puerto)

    def recibirMensaje(self, mensaje):
        self.mensajes_recv.append(mensaje)  #
        self.controlador.escribirMensajeNuevo(mensaje)

    def enviarMensaje(self, mensaje):
        if self.envio.enviarMensaje(mensaje):
            self.mensajes_env.append(mensaje)
            self.controlador.escribirMensajeEnviado(mensaje)
        else:
            self.controlador.mostrarError("Ocurrió un error en el envío")

    def desconectar(self):
        pass


class ConexionEntrante(threading.Thread):
    def __init__(self, ip, puerto):
        threading.Thread.__init__(self)
        self.ip = ip
        self.puerto = puerto
        self.socket = None

    def run(self):
        # Inicializar el socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.puerto))
        # Loop de recepción
        socket_ok = True
        while socket_ok:
            socket_ok = self.recibirMensaje()

    def recibirMensaje(self):
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        cellsRecv = conn.recv(1024).decode('utf-8')
        
        return True # TODO


class ConexionSaliente():
    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto
        self.socket = None  # TODO

    def enviarMensaje(self, mensaje):
        pass  # TODO enviar mensaje al socket.

    
