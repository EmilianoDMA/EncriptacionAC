import sys
import time
import copy
import random
import binascii
import socket
import threading
from pdb import set_trace
from time import sleep
from Modelo.HiloEnvio import HiloEnvio
from Modelo.HiloRecepcion import HiloRecepcion
import pickle


class Modelo:
    puertos_servidor = {
        'send': 9090,  # Socket en el que el servidor espera recibir datos.
        'recv': 8000   # Socket en el que el servidor pone datos para enviar.
    }

    def __init__(self, controlador):
        self.controlador = controlador
        self.lista_mensajes_enviados = []
        self.lista_mensajes_recibidos = []
        self.socket_recep = socket.socket()
        self.socket_recep.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_envio = socket.socket()
        self.socket_envio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mandarDH = 0
        self.calculoIntermedio = 0
        self.secretoCompartido = 0

    def conectar(self, ip_servidor, puerto):
        # Me conecto al servidor
        try:
            self.puerto = puerto
            self.socket_envio.connect((ip_servidor, self.puerto))
            print("Se conectó el stream de envío hacia "+ip_servidor)
            # Espero la conexion del cliente.
            self.socket_recep.bind(('0.0.0.0', self.puerto+1))
            self.socket_recep.listen(1)
            self.cliente, self.direccion = self.socket_recep.accept()
            print("Se conecto el stream de entrada del cliente "+self.direccion[0])
            # A partir de este punto, esta conectado por ambos canales.
            self.hilo_envio = HiloEnvio(self, self.socket_envio)
            self.hilo_recep = HiloRecepcion(self, self.socket_recep, self.cliente)
            self.hilo_envio.start()
            self.hilo_recep.start()
            self.controlador.limpiarMensajes()
        except ConnectionRefusedError:
            self.controlador.deshabilitarVista()
            self.controlador.informarError("No se pudo establecer la conexion")

    def hayMensajesPendientes(self):
        """
        Devuelve si hay o no mensajes pendientes.
        """
        if len(self.lista_mensajes_enviados) > 0:
            return True
        return False

    def getMensajesPendientes(self):
        """
        Devuelve los mensajes pendientes de envío.
        """
        return self.lista_mensajes_enviados

    def enviarMensaje(self, mensaje):
        #Recibe el mensaje y lo pasa a un arreglo de int donde cada posicion es un caracter en su valor UTF-8
        mensajeUTF = list (mensaje.encode('utf-8'))

        #Setea el tiempo máximo que se ejecutara el AC y otras variables
        MAX_TIME = len(mensaje) * 8
        HALF_SIZE = MAX_TIME
        indices = range(-HALF_SIZE, HALF_SIZE+1)

        #Genera un estado inicial aleatorio en Cells para el AC
        print("\n ************ Nuevo Mensaje a Enviar ************")
        print("El mensaje a enviar es: " + mensaje)
        print("Se generará un estado inicial aleatorio para el automata")
        cells = {i: '0' for i in indices}
        for i in cells:
            azar = random.randint(0,1)
            cells[i] = str(azar)        
        cells[-HALF_SIZE-1] = '0' # Llena ambos extremos
        cells[ HALF_SIZE+1] = '0'
        estadoInicial = []
        estadoInicial = cells #Guarda el estado inicial
        print("El Estado Inicial generado aleatoriamente para del automata es: " + str(estadoInicial))

        #Ejecuta el AC
        print("******** EJECUTANDO EL AUTOMATA CELULAR ********")
        new_state = {"111": '0', "110": '0', "101": '0', "000": '0',
                    "100": '1', "011": '1', "010": '1', "001": '1'} #Comportamiento que tendrá
        for time in range(0, MAX_TIME): #Ejecucion
            patterns = {i: cells[i-1] + cells[i] + cells[i+1] for i in
                        indices}
            cells = {i: new_state[patterns[i]] for i in indices}
            cells[-HALF_SIZE-1] = '0'
            cells[ HALF_SIZE+1] = '0'
        print("LISTO")
        #Creación de la máscara a partir del último estado (cells) del AC. La mascara es un arreglo de enteros decimales.
        #Para crear la máscara, se utiliza Cells (binario) tomando de a 8 bits y se pasandolos a su equivalente decimal dando como resultado un arreglo.
        arregloDividido = []
        concat = ""
        bitCant = 1
        for y in cells:
            concat =  concat + str(cells[y])
            if bitCant == 8:
                arregloDividido.append(concat)
                bitCant = 0
                concat = ""
            bitCant = bitCant + 1
        mascara = []
        i = 0
        for i in arregloDividido:
            mascara.append(int(i, 2))
        y = 0

        #CIFRADO. Se cifra haciendo un XOR elemento a elemento entre la mascara y el mensaje (ambos como arreglos de enteros decimales).
        print("Se cifrará el mensaje a enviar utilizando el último estado del AC para generar una máscara")
        arregloCifrado = []
        indice = 0
        print("El mensaje a cifrar en UTF es: " + str(mensajeUTF))
        print("La máscara generada por el automata es: " + str(mascara))
        for m in mensajeUTF:
            arregloCifrado.append((m ^ mascara[indice]))
            indice = indice + 1 
        print("** CIFRADO **")
        print("EL MENSAJE CIFRADO ES: " + str(arregloCifrado) + "\n")

        mensajeArray = []
        mensajeArray.append(str(MAX_TIME))
        #estadoEnvCifrado = (int(estadoEnvStr,2)) ^ self.secretoCompartido

        secretoCompartidoBits = bin(self.secretoCompartido)
        print("El Secreto Compartido expresado en bits es: " + str(secretoCompartidoBits))
        print("SE CIFRARÁ EL ESTADO INICIAL CON EL SECRETO COMPARTIDO ACORDADO POR DIFFIE-HELLMAN PARA ENVIARLO POR LA RED")
        v = 2 #Inicia en 2 porque el str del binario da en formato 0bxxxxx y debemos omitir el "0b"
        for b in estadoInicial:
            estadoInicial[b] = int(estadoInicial[b]) ^ int(secretoCompartidoBits[v])
            v = v + 1
            if v == len(secretoCompartidoBits):
                v = 2 #Inicia en 2 porque el str del binario da en formato 0bxxxxx y debemos omitir el "0b"
        print("El Estado Inicial cifrado es: " + str(estadoInicial))

        mensajeArray.append(pickle.dumps(estadoInicial)) 
        mensajeArray.append(str(len(arregloCifrado)))
        mensajeArray.append(pickle.dumps(arregloCifrado))

        arregloSerialzado = pickle.dumps(mensajeArray)
        
        print("** Enviando el mensaje cifrado junto con el estado inicial del AC cifrado y otros datos para el descifrado del mensaje **")
        self.lista_mensajes_enviados.append(arregloSerialzado)
        print("************ Fin proceso de envío ************\n")

    def recibirMensaje(self, arregloSerialzado):
        #Recibe tiempo que se ejecutará el AC

        arregloMensaje = pickle.loads(arregloSerialzado)

        MAX_TIME = int(arregloMensaje[0])

        #Recibe estado inicial
        estadoInicial = pickle.loads(arregloMensaje[1])
        secretoCompartidoBits = bin(self.secretoCompartido)
        print("El Secreto Compartido expresado en bits es: " + str(secretoCompartidoBits))
        print("SE DESCIFRARÁ EL ESTADO INICIAL CON EL SECRETO COMPARTIDO ACORDADO POR DIFFIE-HELLMAN PARA RECREAR EL AC")
        v = 2 #Inicia en 2 porque el str del binario da en formato 0bxxxxx y debemos omitir el "0b"
        print("El Estado Inicial cifrado es: " + str(estadoInicial))
        for b in estadoInicial:
            estadoInicial[b] = str(int(estadoInicial[b]) ^ int(secretoCompartidoBits[v]))
            v = v + 1
            if v == len(secretoCompartidoBits):
                v = 2 #Inicia en 2 porque el str del binario da en formato 0bxxxxx y debemos omitir el "0b"
        print("El Estado Inicial descifrado es: " + str(estadoInicial))

        #Recibe el largo del mensaje encriptado
        maxLoop = int(arregloMensaje[2])

        #Recibe el mensaje encriptado
        mensajeCifrado = pickle.loads(arregloMensaje[3])
        print("El mensaje cifrado recibido es: " + str(mensajeCifrado))

        #Setea el tiempo recibido y otras variables
        HALF_SIZE = MAX_TIME
        indices = range(-HALF_SIZE, HALF_SIZE+1)
        #Setea el estado inicial recibido para ejecutar el AC
      
        print("******** EJECUTANDO EL AUTOMATA CELULAR ********")
        cells = estadoInicial
        #Ejecuta el AC y genera la mascara a partir del estado final
        new_state = {"111": '0', "110": '0', "101": '0', "000": '0',
        "100": '1', "011": '1', "010": '1', "001": '1'} #Comportamiento que tendrá
        for time in range(0, MAX_TIME): #Ejecucion
            patterns = {i: cells[i-1] + cells[i] + cells[i+1] for i in
                indices}
            cells = {i: new_state[patterns[i]] for i in indices}
            cells[-HALF_SIZE-1] = '0'
            cells[ HALF_SIZE+1] = '0'
        print("LISTO")
        print("Se descifrará el mensaje utilizando el último estado del AC recreado para generar una máscara")
        #Pasa la mascara de binario a un arreglo de enteros decimales (tomando de a 8 bits)
        arregloDividido = []
        concat = ""
        bitCant = 1
        for y in cells:
            concat =  concat + str(cells[y])
            if bitCant == 8:
                arregloDividido.append(concat)
                bitCant = 0
                concat = ""
            bitCant = bitCant + 1
        mascara = []
        i = 0
        for i in arregloDividido:
            mascara.append(int(i, 2))
        y = 0

        print("La máscara generada por el automata es: " + str(mascara))

        #DESCIFRADO. Se descifra haciendo XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje cifrado, ambos siendo arreglos de enteros decimales.
        #Se obtiene, asi, el mensaje original en forma de un arreglo de enteros. El contenido de este arreglo son los caracteres del mensaje original en sus valores UTF-8.
        arregloDescifrado = []
        indice = 0

        for m in mensajeCifrado:
            arregloDescifrado.append((m ^ mascara[indice]))
            indice = indice + 1
        
        print("**DESCIFRADO**")

        #Se decodifica el arreglo, obteniendo finalmente el mensaje original.
        print("El mensaje descifrado en UTF es: " + str(arregloDescifrado))
        cadena = bytes(arregloDescifrado)
        textoDescifrado = cadena.decode('utf-8')
        print("El mensaje descifrado es: " + str(textoDescifrado))
        
        self.controlador.recibirMensaje(textoDescifrado)
        print("************ Fin proceso de recepción ************")

        return True  # TODO

    def desconectar(self):
        self.hilo_envio.desconectar()
        self.hilo_recep.desconectar()
