# -*- coding: utf-8 -*-

import sys
import time
import socket
import threading
import random
from HiloCliente import HiloCliente
# TODO: Hay que sacar esto del proyecto cliente a un nuevo proyecto servidor.

class Servidor:

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
        self.moduloDH = random.randint(1000,5000)
        self.nroCompartidoDH = random.randint(1000,5000)
        self.mandarDH1 = 0
        self.mandarDH2 = 0
        self.cliente1 = HiloCliente(self, Servidor.puertos_cliente1, self.id_cliente_1, self.moduloDH, self.nroCompartidoDH)
        self.cliente2 = HiloCliente(self, Servidor.puertos_cliente2, self.id_cliente_2, self.moduloDH, self.nroCompartidoDH)

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

    def setMandarDH(self, calc, id):
        if id == 1:
            self.mandarDH1 = calc
        else:
            self.mandarDH2 = calc

    def getMandarDH(self, id):
        if id == 1:
            return self.mandarDH2
        else:
            return self.mandarDH1
           
if __name__ == '__main__':
    s = Servidor()
