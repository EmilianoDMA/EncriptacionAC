import sys
import time
import copy
import random
import binascii
import socket
import threading
from pdb import set_trace
from time import sleep
from Modelo.HiloEnvio import HiloEnvio
from Modelo.HiloRecepcion import HiloRecepcion


class Modelo:
    puertos_servidor = {
        'send': 9090,  # Socket en el que el servidor espera recibir datos.
        'recv': 8000   # Socket en el que el servidor pone datos para enviar.
    }

    def __init__(self, controlador):
        self.controlador = controlador
        self.lista_mensajes_enviados = []
        self.lista_mensajes_recibidos = []
        self.socket_recep = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_envio = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def conectar(self, ip_servidor, puerto):
        # Me conecto al servidor
        try:
            self.puerto = puerto
            self.socket_envio.connect((ip_servidor, self.puerto))
            print("Se conectó el stream de envío hacia "+ip_servidor)
            # Espero la conexion del cliente.
            self.socket_recep.bind(('0.0.0.0', self.puerto+1))
            self.socket_recep.listen(1)
            self.cliente, self.direccion = self.socket_recep.accept()
            print("Se conecto el stream de entrada del cliente "+self.direccion[0])
            # A partir de este punto, esta conectado por ambos canales.
            self.hilo_envio = HiloEnvio(self, self.socket_envio)
            self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
            self.hilo_envio.start()
            self.hilo_recep.start()
            self.controlador.limpiarMensajes()
        except ConnectionRefusedError:
            self.controlador.deshabilitarVista()
            self.controlador.informarError("No se pudo establecer la conexion")

    def hayMensajesPendientes(self):
        """
        Devuelve si hay o no mensajes pendientes.
        """
        if len(self.lista_mensajes_enviados) > 0:
            return True
        return False

    def getMensajesPendientes(self):
        """
        Devuelve los mensajes pendientes de envío.
        """
        return self.lista_mensajes_enviados

    def recibirMensaje(self, mensaje):
        """
        Ingresa un mensaje nuevo recibido.
        """
        self.controlador.recibirMensaje(mensaje)
        self.lista_mensajes_recibidos.append(mensaje)

    def enviarMensaje(self, mensaje):
        """
        Agrega un mensaje a la lista de pendientes de enviar
        """
        self.lista_mensajes_enviados.append(mensaje)

    def desconectar(self):
        pass
