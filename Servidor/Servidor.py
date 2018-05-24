# -*- coding: utf-8 -*-

import socket, sys, threading, time

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
        self.lista_mensajes1 = []
        self.lista_mensajes2 = []

        self.start()

    def start(self):
        self.cliente1 = HiloCliente(self, Servidor.puertos_cliente1, 1)
        self.cliente2 = HiloCliente(self, Servidor.puertos_cliente2, 2)
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
        if id == 1:
            self.lista_mensajes1.append(mensaje)
        else:
            self.lista_mensajes2.append(mensaje)

class HiloCliente(threading.Thread):
    def __init__(self, servidor, puertos, id):
        threading.Thread.__init__(self)
        self.id = id
        self.servidor = servidor
        self.puertos = puertos
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
        self.hilo_envio = HiloEnvio(self, self.socket_envio)
        self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
        self.hilo_envio.start()
        self.hilo_recep.start()
        
        while True:
            pass

    def hayMensajesPendientes(self):
        return self.servidor.hayMensajesPendientes(self.id)

    def getMensajesPendientes(self):
        return self.servidor.getMensajesPendientes(self.id)

    def mensajeNuevoRecibido(self, mensaje):
        self.servidor.mensajeNuevoRecibido(mensaje, self.id)

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


if __name__ == '__main__':
    s = Servidor()
