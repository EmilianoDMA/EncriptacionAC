# -*- coding: utf-8 -*-

import socket, sys, threading, time

class Servidor:
    puertos_cliente1 = {
        'recv': 8080,
        'send': 8000
    }
    puertos_cliente2 = {
        'recv': 9090,
        'send': 9000
    }

    def __init__(self):
        self.lista_mensajes1 = []
        self.lista_mensajes2 = []

        self.start()

    def start(self):
        self.cliente1 = HiloCliente(self, Servidor.puertos_cliente1)
        self.cliente2 = HiloCliente(self, Servidor.puertos_cliente2)
        self.cliente1.start()
        self.cliente2.start()

    def getMensajesPendientes(self, puerto):
        if puerto == Servidor.puertos_cliente1["recv"]:
            return self.lista_mensajes1
        else:
            return self.lista_mensajes2

    def hayMensajesPendientes(self, puerto):
        if puerto == Servidor.puertos_cliente1["recv"]:
            if len(self.lista_mensajes1) > 0:
                return True
            return False
        else:
            if len(self.lista_mensajes2) > 0:
                return True
            return False

    def mensajeNuevoRecibido(self, mensaje, puerto):
        if puerto == Servidor.puertos_cliente1["recv"]:
            self.lista_mensajes1.append(mensaje)
        else:
            self.lista_mensajes2.append(mensaje)

class HiloCliente(threading.Thread):
    def __init__(self, servidor, puertos):
        threading.Thread.__init__(self)
        self.servidor = servidor
        self.socket_recep = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_envio = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Espero la conexion del cliente.
        self.socket_recep.bind(('0.0.0.0', puertos['recv']))
        self.socket_recep.listen(1)
        self.cliente, self.direccion = self.socket_recep.accept()
        print("Se conecto el stream de entrada del cliente "+self.direccion[0])
        # Me conecto al servidor
        self.socket_envio.connect((self.direccion[0], puertos['send']))
        print("Se conectó el stream de envío al cliente "+self.direccion[0])
        # A partir de este punto, esta conectado por ambos canales.
        self.hilo_envio = HiloEnvio(self, self.socket_envio)
        self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
        self.hilo_envio.start()
        self.hilo_recep.start()

    def run(self):
        while True:
            pass

class HiloEnvio(threading.Thread):
    def __init__(self, servidor, socket):
        threading.Thread.__init__(self)
        self.servidor = servidor
        self.socket = socket
        print("## Iniciando el hilo de envío")

    def run(self):
        while True:
            time.sleep(1)
            if self.servidor.hayMensajesPendientes(self.servidor.puertos["recv"]):
                mensajes = self.servidor.getMensajesPendientes(self.servidor.puertos["recv"])
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
            #self.servidor.mensajeNuevoRecibido(mensaje.decode(), self.servidor.puertos["recv"])
            print(mensaje)


if __name__ == '__main__':
    s = Servidor()
