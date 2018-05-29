# -*- coding: utf-8 -*-

import sys
import time
import socket
import threading
from HiloCliente import HiloCliente
# TODO: Hay que sacar esto del proyecto cliente a un nuevo proyecto servidor.

class Servidor:
    """
    TODO: Nota a futuro porque me quedo sin batería
    Definir la tupla socket_recv, socket_snd base y a partir de ahí, asignar a cada dupla de clientes los sockets para
    que sepan por donde comunicarse (En lugar de los hardcodeados).
    """
    puertos_cliente1 = {
        'recv': 8080,
        'send': 8081
    }
    puertos_cliente2 = {
        'recv': 9090,
        'send': 9091
    }

    def __init__(self):
        self.id_cliente_1 = 1
        self.id_cliente_2 = 2
        self.lista_mensajes1 = []
        self.lista_mensajes2 = []
        self.cliente1 = HiloCliente(self, Servidor.puertos_cliente1, self.id_cliente_1)
        self.cliente2 = HiloCliente(self, Servidor.puertos_cliente2, self.id_cliente_2)

        self.start()

    def start(self):
        self.cliente1.start()
        self.cliente2.start()
 
    def getMensajesPendientes(self, id):
        if id == 1:
            return self.lista_mensajes2
        else:
            return self.lista_mensajes1

    def hayMensajesPendientes(self, id):
        if id == 1:
            if len(self.lista_mensajes2) > 0:
                return True
            return False
        else:
            if len(self.lista_mensajes1) > 0:
                return True
            return False

    def mensajeNuevoRecibido(self, mensaje, id):
        print("El cliente "+str(id)+" envió el mensaje: ")
        print(mensaje)
        if id == 1:
            self.lista_mensajes1.append(mensaje)
        else:
            self.lista_mensajes2.append(mensaje)


if __name__ == '__main__':
    s = Servidor()
