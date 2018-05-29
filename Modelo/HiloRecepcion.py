# -*- coding: utf-8 -*-

import time
import socket
import threading


class HiloRecepcion(threading.Thread):
    def __init__(self, obj_cliente, socket, cliente):
        threading.Thread.__init__(self)
        self.obj_cliente = obj_cliente
        self.socket = socket
        self.cliente = cliente
        print("## Iniciando el hilo de recepción")

    def run(self):
        while True:
            mensaje = self.cliente.recv(1024)
            self.obj_cliente.recibirMensaje(mensaje.decode())
            print("Recibí : " + str(mensaje.decode()))
