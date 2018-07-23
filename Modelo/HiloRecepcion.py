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
        print("Calculo finalizado.")
        print("El secreto compartido es: " + str(self.obj_cliente.secretoCompartido))
        print("******* Fin Diffie-Hellman ********\n")
        print("******* Conexión con el usuario establecida ********\n")
        while True:
            mensaje = self.cliente.recv(90000)
            #self.obj_cliente.recibirMensaje(mensaje.decode())
            print(" ************ Nuevo Mensaje Recibido ************")
            print("Recibí : " + str(mensaje))
            self.obj_cliente.recibirMensaje(mensaje)

    #Este es el Diffie-Hellman del Cliente. 
    #El cliente recibe los numeros acordados por el servidor
    #El nro secreto se calcula en el Diffie-Hellman de los clientes.    
    def diffieHellman(self, hilo):
        print("\n******* Inicio Diffie-Hellman ********")
        numeroSecreto = random.randint(0,5000)
        print("Mi numero secreto es: " + str(numeroSecreto))
        
        numerosAcordados = self.cliente.recv(1024).decode()

        numeroComun = int(numerosAcordados[0:4])
        print("El numero común es: " + str(numeroComun))
        modulo = int(numerosAcordados[4:8])
        print("El modulo acordado es: " + str(modulo))

        calculoIntermedio = numeroComun ** numeroSecreto % modulo
        hilo.obj_cliente.calculoIntermedio = calculoIntermedio

        computar = int(self.cliente.recv(1024).decode())

        secretoCompartido = computar**numeroSecreto % modulo
        return secretoCompartido

    def desconectar(self):
        self.socket.close()
