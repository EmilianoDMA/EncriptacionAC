# -*- coding: utf-8 -*-

import time
import socket
import threading


class HiloEnvio(threading.Thread):
    def __init__(self, padre, socket):
        threading.Thread.__init__(self)
        self.padre = padre
        self.socket = socket
        print("## Iniciando el hilo de envío")

    def run(self):
        while True:
            time.sleep(1)
            if self.padre.hayMensajesPendientes():
                mensajes = self.padre.getMensajesPendientes()
                print("Hay "+str(len(mensajes))+" mensajes pendientes para el cliente "+str(self.padre.id))
                for mensaje in mensajes:
                    self.socket.send(mensaje.encode())
            else:
                print("No hay mensajes pendientes para el cliente "+str(self.padre.id))
