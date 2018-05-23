# -*- coding: utf-8 -*-

import socket, sys, threading, time

class Servidor:
    puertos_cliente = {
        'recv': 8080,
        'send': 8000
    }

    def __init__(self):
        self.lista_mensajes = []
        self.socket_recep = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_envio = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()

    def start(self):
        # Espero la conexion del cliente.
        self.socket_recep.bind(('0.0.0.0', Servidor.puertos_cliente['recv']))
        self.socket_recep.listen(1)
        self.cliente, self.direccion = self.socket_recep.accept()
        print("Se conecto el stream de entrada del cliente "+self.direccion[0])
        # Me conecto al servidor
        self.socket_envio.connect((self.direccion[0], Servidor.puertos_cliente['send']))
        print("Se conectó el stream de envío al cliente "+self.direccion[0])
        # A partir de este punto, esta conectado por ambos canales.
        self.hilo_envio = HiloEnvio(self, self.socket_envio)
        self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
        self.hilo_envio.start()
        self.hilo_recep.start()

    def getMensajesPendientes(self):
        return self.lista_mensajes

    def hayMensajesPendientes(self):
        if len(self.lista_mensajes) > 0:
            return True
        return False

    def mensajeNuevoRecibido(self, mensaje):
        self.lista_mensajes.append(mensaje)


class HiloEnvio(threading.Thread):
    def __init__(self, servidor, socket):
        threading.Thread.__init__(self)
        self.servidor = servidor
        self.socket = socket
        print("## Iniciando el hilo de envío")

    def run(self):
        while True:
            time.sleep(1)
            if self.servidor.hayMensajesPendientes():
                mensajes = self.servidor.getMensajesPendientes()
                for mensaje in mensajes:
                    self.socket.send(mensaje.encode())
            else:
                print("No hay mensajes pendientes")


class HiloRecepcion(threading.Thread):
    def __init__(self, servidor, socket, cliente):
        threading.Thread.__init__(self)
        self.servidor = servidor
        self.socket = socket
        self.cliente = cliente
        print("## Iniciando el hilo de recepción")

    def run(self):
        while True:
            mensaje = self.cliente.recv(1024)
            #self.servidor.mensajeNuevoRecibido(mensaje.decode())
            print(mensaje)


if __name__ == '__main__':
    s = Servidor()
