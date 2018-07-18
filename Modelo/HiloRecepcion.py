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
        print("El secreto compartido es: " + str(self.obj_cliente.secretoCompartido))
        while True:
            mensaje = self.cliente.recv(90000)
            #self.obj_cliente.recibirMensaje(mensaje.decode())
            self.obj_cliente.recibirMensaje(mensaje)
            print("Recibí : " + str(mensaje))

    #Este es el Diffie-Hellman del Cliente. 
    #El cliente recibe los numeros acordados por el servidor
    #El nro secreto se calcula en el Diffie-Hellman de los clientes.    
    def diffieHellman(self, hilo):
        numeroSecreto = random.randint(0,5000)
        print("Mi numero secreto es: " + str(numeroSecreto))
        
        numerosAcordados = self.cliente.recv(1024).decode()
        print("Los numeros acordados son: " + numerosAcordados)

        numeroComun = int(numerosAcordados[0:4])
        print("El numero comun es: " + str(numeroComun))
        modulo = int(numerosAcordados[4:8])
        print("el modulo es: " + str(modulo))

        #numeroComun = int(self.cliente.recv(1024).decode())
        #print("El numero comun es: " + str(numeroComun))
        #modulo = int(self.cliente.recv(1024).decode())
        #print("el modulo es: " + str(modulo))


        calculoIntermedio = numeroComun ** numeroSecreto % modulo
        print("Se va a settear mandarDH (calculo intermedio): " + str(calculoIntermedio))
        hilo.obj_cliente.calculoIntermedio = calculoIntermedio
        print("Seteado")

        computar = int(self.cliente.recv(1024).decode())

        secretoCompartido = computar**numeroSecreto % modulo
        return secretoCompartido
