# -*- coding: utf-8 -*-

import time
import socket
import threading
import random

class HiloRecepcion(threading.Thread):
    def __init__(self, obj_cliente, socket, cliente):
        threading.Thread.__init__(self)
        self.obj_cliente = obj_cliente
        self.socket = socket
        self.cliente = cliente
        print("## Iniciando el hilo de recepción")

    def run(self):
        self.obj_cliente.secretoCompartido = self.diffieHellman(self)
        print("El secreto compartido es" + str(self.obj_cliente.secretoCompartido))
        while True:
            mensaje = self.cliente.recv(1024)
            self.obj_cliente.recibirMensaje(mensaje.decode())
            print("Recibí : " + str(mensaje.decode()))

    #Este es el Diffie-Hellman del Cliente. 
    #El cliente recibe los numeros acordados por el servidor
    #El nro secreto se calcula en el Diffie-Hellman de los clientes.
    def diffieHellman(self, hilo):
        numeroSecreto = random.randint(0,5000)
        numeroComun = int(self.cliente.recv(1024).decode())
        modulo = int(self.cliente.recv(1024).decode())

        mandar = numeroComun ** numeroSecreto % modulo

        hilo.obj_cliente.mandarDH = mandar

        computar = int(self.cliente.recv(1024).decode())

        secretoCompartido = computar**numeroSecreto % modulo
        return secretoCompartido
