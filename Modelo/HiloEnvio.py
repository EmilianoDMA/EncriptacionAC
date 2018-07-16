# -*- coding: utf-8 -*-

import time
import socket
import threading

class HiloEnvio(threading.Thread):
    def __init__(self, obj_cliente, socket):
        threading.Thread.__init__(self)
        self.obj_cliente = obj_cliente
        self.socket = socket
        print("## Iniciando el hilo de envío")

    def run(self):
        self.diffieHellman()
        mensajeMostrado = False
        while True:
            time.sleep(1)
            if self.obj_cliente.hayMensajesPendientes():
                mensajes = self.obj_cliente.getMensajesPendientes()
                for mensaje in mensajes:
                    self.socket.send(mensaje)
                    mensajes.pop()
                mensajeMostrado = False
            else:
                if mensajeMostrado == False:
                    print("No hay mensajes pendientes")
                    mensajeMostrado = True
    
    def diffieHellman(self):
        while self.obj_cliente.calculoIntermedio == 0:
            pass
        self.socket.send((str(self.obj_cliente.calculoIntermedio)).encode())

        