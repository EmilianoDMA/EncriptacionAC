# -*- coding: utf-8 -*-

import time
import socket
import threading


class HiloEnvio(threading.Thread):
    def __init__(self, padre, socket, numeroComun, modulo):
        threading.Thread.__init__(self)
        self.numeroComun = numeroComun
        self.modulo = modulo
        self.padre = padre
        self.socket = socket
        print("## Iniciando el hilo de envío")

    def run(self):
        self.diffieHellman(self.numeroComun, self.modulo)
        while True:
            time.sleep(1)
            if self.padre.hayMensajesPendientes():
                mensajes = self.padre.getMensajesPendientes()
                print("Hay "+str(len(mensajes))+" mensajes pendientes para el cliente "+str(self.padre.id))
                for mensaje in mensajes:
                    self.socket.send(mensaje.encode())
                    mensajes.pop()
            else:
                print("No hay mensajes pendientes para el cliente "+str(self.padre.id))
    
#Este es el Diffie-Hellman del Servidor donde SOLO se envían los numeros acordados (y un nro intermedio recibido en el hilo recept)
#El servidor no tiene que saber el Nro Secreto, pero elige los numeros acordados a los clientes
#El nro secreto se calcula en el Diffie-Hellman de los clientes.
    def diffieHellman(self, numeroComun, modulo):
        numerosAcordados = str(numeroComun) + str(modulo)
        #self.socket.send((str(numeroComun)).encode())
        #print("MANDAO EL NUMERO COMUN:" + str(numeroComun))
        #self.socket.send((str(modulo)).encode())
        #print("el modulo es: " + str(modulo))
        self.socket.send(numerosAcordados.encode())
        print("El numero Acordado es: " + numerosAcordados)
        while self.padre.getMandarDH() == 0:
            pass
        print("CHWQUEO: " + str(self.padre.getMandarDH()))
        self.socket.send((str(self.padre.getMandarDH())).encode())