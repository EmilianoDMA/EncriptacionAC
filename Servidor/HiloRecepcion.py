# -*- coding: utf-8 -*-

import time
import socket
import threading
import math


class HiloRecepcion(threading.Thread):
    def __init__(self, padre, socket, cliente):
        threading.Thread.__init__(self)
        self.padre = padre
        self.socket = socket
        self.cliente = cliente
        print("## Iniciando el hilo de recepción")

    def run(self):
        self.padre.setMandarDH(self.diffieHellman())
        while True:
            tam = int((self.cliente.recv(1024)).decode())
            veces = 0
            veces = math.ceil(tam/1024)
            mensaje = b''
            for j in range(0, veces):
                msj = self.cliente.recv(1024)
                mensaje += msj
            self.padre.mensajeNuevoRecibido(mensaje)
            print(mensaje)

    #Este es el Diffie-Hellman del Servidor donde SOLO solo recive. 
    #El servidor no tiene que saber el Nro Secreto, pero elige los numeros acordados a los clientes
    #El nro secreto se calcula en el Diffie-Hellman de los clientes.
    def diffieHellman(self):
        calculoIntermedio = int((self.cliente.recv(1024)).decode())
        return calculoIntermedio