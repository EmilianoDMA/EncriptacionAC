# -*- coding: utf-8 -*-

import socket
import threading
from HiloEnvio import HiloEnvio
from HiloRecepcion import HiloRecepcion

class HiloCliente(threading.Thread):
    def __init__(self, servidor, puertos, id, moduloDH, compartidoDH):
        threading.Thread.__init__(self)
        self.id = id
        self.servidor = servidor
        self.puertos = puertos
        self.moduloDH = moduloDH
        self.mandarDH = 0
        self.compartidoDH = compartidoDH
        self.socket_recep = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_envio = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Iniciado el servidor de escucha en el puerto "+str(puertos['recv']))

    def run(self):
        # Espero la conexion del cliente.
        self.socket_recep.bind(('0.0.0.0', self.puertos['recv']))
        self.socket_recep.listen(1)
        self.cliente, self.direccion = self.socket_recep.accept()
        print("Se conecto el stream de entrada del cliente "+self.direccion[0]+" en el puerto "+str(self.puertos['recv']))
        # Me conecto al servidor
        self.socket_envio.connect((self.direccion[0], self.puertos['send']))
        print("Se conectó el stream de envío al cliente "+self.direccion[0]+" en el puerto "+str(self.puertos['send']))
        # A partir de este punto, esta conectado por ambos canales.
        self.hilo_envio = HiloEnvio(self, self.socket_envio, self.moduloDH, self.compartidoDH)
        self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
        self.hilo_envio.start()
        self.hilo_recep.start()

        while True:
            if not self.hilo_envio.is_alive() or not self.hilo_recep.is_alive():
                break 

    def hayMensajesPendientes(self):
        return self.servidor.hayMensajesPendientes(self.id)

    def getMensajesPendientes(self):
        return self.servidor.getMensajesPendientes(self.id)

    def mensajeNuevoRecibido(self, mensaje):
        self.servidor.mensajeNuevoRecibido(mensaje, self.id)

"""
    def DiffieHellman(self, numeroComun, modulo):
        numeroSecreto = random.randint(0,5000)
        mandar = numeroComun ** numeroSecreto % modulo

        self.socket.send(str(mandar).encode('utf-8'))
        computar = int(self.socket.recv(1024).decode('utf-8'))

        self.numeroSecretoEnvio = computar**numeroSecreto % modulo
        return self.numeroSecretoEnvio


    def DiffieHellman(self,conn):
        numeroSecreto = random.randint(0,5000)
        mandar = numeroComun ** numeroSecreto % modulo
        
        computar = int(conn.recv(1024).decode('utf-8'))
        conn.send(str(mandar).encode('utf-8'))

        self.numeroSecretoRecibo = computar**numeroSecreto % modulo
"""