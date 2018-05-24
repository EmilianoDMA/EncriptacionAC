# -*- coding: utf-8 -*-

import time
import socket
import threading


class HiloRecepcion(threading.Thread):
    def __init__(self, padre, socket, cliente):
        threading.Thread.__init__(self)
        self.padre = padre
        self.socket = socket
        self.cliente = cliente
        print("## Iniciando el hilo de recepción")

    def run(self):
        while True:
            mensaje = self.cliente.recv(1024)
            self.padre.mensajeNuevoRecibido(mensaje.decode())
            print(mensaje)
