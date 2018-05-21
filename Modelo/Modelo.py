import sys
import random
import binascii
import socket
import threading
from pdb import set_trace
from time import sleep



class Modelo():
    def __init__(self, controlador):
        self.controlador = controlador
        self.envio = None
        self.recep = None
        self.mensajes_recv = []
        self.mensajes_env = []

    def conectar(self, ip, puerto):
        # TODO Crear la conexion en su propio hilo
        self.recep = ConexionEntrante(self, ip, puerto)
        # TODO Crear la conexion en su propio hilo
        self.envio = ConexionSaliente(self, ip, puerto)

    def recibirMensaje(self, mensaje):
        self.mensajes_recv.append(mensaje)  
        self.controlador.recibirMensaje(mensaje)

    def enviarMensaje(self, mensaje):
        if self.envio.enviarMensaje(mensaje):
            self.mensajes_env.append(mensaje)
            self.controlador.escribirMensajeEnviado(mensaje)
        else:
            self.controlador.mostrarError("Ocurrió un error en el envío")

    def desconectar(self):
        self.envio.desconectarSaliente()


class ConexionEntrante(threading.Thread):
    def __init__(self, modelo, ip, puerto):
        threading.Thread.__init__(self)
        self.modelo = modelo
        self.ip = ip
        self.puerto = puerto
        self.socket = None
        self.numeroSecretoRecibo = 0

    def run(self):
        # Inicializar el socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.puerto))
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        #Clave por DiffieHellman
        self.DiffieHellman()           
        # Loop de recepción
        socket_ok = True
        while socket_ok:
            socket_ok = self.recibirMensaje()
        conn.close()

    def recibirMensaje(self):
        #Recibe tiempo que se ejecutará el AC
        MAX_TIME = int(conn.recv(1024).decode('utf-8'))

        #Recibe estado inicial
        cellsRecvCifrado = conn.recv((MAX_TIME * 2)+1).decode('utf-8')
        cellsRecv = bin(int(cellsRecvCifrado) ^ self.numeroSecretoRecibo)

        #Recibe el largo del mensaje encriptado
        maxLoop = int(conn.recv(1024).decode('utf-8'))

        #Recibe el mensaje encriptado
        mensajeCifrado = []
        for x in range(0, maxLoop):
            aux = int(conn.recv(1024).decode('utf-8'))
            mensajeCifrado.append(aux)

        #Setea el tiempo recibido y otras variables
        HALF_SIZE = MAX_TIME
        indices = range(-HALF_SIZE, HALF_SIZE+1)
        #Setea el estado inicial recibido para ejecutar el AC
        cells = {i: '0' for i in indices}
        cont = 2
        for i in cells:
            valor = cellsRecv[cont]
            cont = cont + 1
            cells[i] = str(valor)
        cells[-HALF_SIZE-1] = '0' # Llena ambos extremos
        cells[ HALF_SIZE+1] = '0'
        estadoInicial = []

        #Ejecuta el AC y genera la mascara a partir del estado final
        new_state = {"111": '0', "110": '0', "101": '0', "000": '0',
        "100": '1', "011": '1', "010": '1', "001": '1'} #Comportamiento que tendrá
        for time in range(0, MAX_TIME): #Ejecucion
            patterns = {i: cells[i-1] + cells[i] + cells[i+1] for i in
                indices}
            cells = {i: new_state[patterns[i]] for i in indices}
            cells[-HALF_SIZE-1] = '0'
            cells[ HALF_SIZE+1] = '0'

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

        #DESCIFRADO. Se descifra haciendo XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje cifrado, ambos siendo arreglos de enteros decimales.
        #Se obtiene, asi, el mensaje original en forma de un arreglo de enteros. El contenido de este arreglo son los caracteres del mensaje original en sus valores UTF-8.
        arregloDescifrado = []
        indice = 0
        for m in mensajeCifrado:
            arregloDescifrado.append((m ^ mascara[indice]))
            indice = indice + 1

        #Se decodifica el arreglo, obteniendo finalmente el mensaje original.
        cadena = bytes(arregloDescifrado)
        textoDescifrado = cadena.decode('utf-8')
        
        self.modelo.recibirMensaje(textoDescifrado)

        return True # TODO

    def DiffieHellman(self):
        numeroSecreto = random.randint(0,5000)
        numeroComun = int(conn.recv(1024).decode('utf-8'))
        modulo = int(conn.recv(1024).decode('utf-8'))
        # RECIBE computar
        computar = int(conn.recv(1024).decode('utf-8'))
        mandar = numeroComun ** numeroSecreto % modulo
        # MANDA mandar
        conn.send(str(mandar).encode('utf-8'))
        self.numeroSecretoRecibo = computar**numeroSecreto % modulo



class ConexionSaliente():
    def __init__(self, modelo, ip, puerto):
        self.modelo = modelo
        self.ip = ip
        self.puerto = puerto
        self.socket = None  # TODO
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.puerto))
        self.numeroSecretoEnvio = 0
        self.DiffieHellman()

    def DiffieHellman(self):
        numeroComun = random.randint(0,5000)
        modulo = random.randint(0,5000)
        numeroSecreto = random.randint(0,5000)

        self.socket.send(numeroComun)
        self.socket.send(modulo)
       
        mandar = numeroComun ** numeroSecreto % modulo

        self.socket.send(str(mandar).encode('utf-8'))
        # RECIBE computar
        computar = int(self.socket.recv(1024).decode('utf-8'))

        self.numeroSecretoEnvio = computar**numeroSecreto % modulo

    def enviarMensaje(self, mensaje):
        #Recibe el mensaje y lo pasa a un arreglo de int donde cada posicion es un caracter en su valor UTF-8
        mensajeUTF = list (mensaje.encode('utf-8'))

        #Setea el tiempo máximo que se ejecutara el AC y otras variables
        MAX_TIME = len(mensaje) * 8
        HALF_SIZE = MAX_TIME
        indices = range(-HALF_SIZE, HALF_SIZE+1)

        #Genera un estado inicial aleatorio en Cells para el AC
        cells = {i: '0' for i in indices}
        for i in cells:
            azar = random.randint(0,1)
            cells[i] = str(azar)        
        cells[-HALF_SIZE-1] = '0' # Llena ambos extremos
        cells[ HALF_SIZE+1] = '0'
        estadoInicial = []
        estadoInicial = cells #Guarda el estado inicial
        #Convierte el estado inicial a Str para que sea más facil la interpretación en pasos posteriores.
        estadoEnv = []
        for i in estadoInicial:
            estadoEnv.append(estadoInicial[i])
        estadoEnvStr = ''.join(estadoEnv)

        #Ejecuta el AC
        new_state = {"111": '0', "110": '0', "101": '0', "000": '0',
                    "100": '1', "011": '1', "010": '1', "001": '1'} #Comportamiento que tendrá
        for time in range(0, MAX_TIME): #Ejecucion
            patterns = {i: cells[i-1] + cells[i] + cells[i+1] for i in
                        indices}
            cells = {i: new_state[patterns[i]] for i in indices}
            cells[-HALF_SIZE-1] = '0'
            cells[ HALF_SIZE+1] = '0'

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
        arregloCifrado = []
        indice = 0
        for m in mensajeUTF:
            arregloCifrado.append((m ^ mascara[indice]))
            indice = indice + 1 

        # ENVIO. Envia los datos necesarios al descifrador.
        HOST = self.ip
        PORT = self.puerto

        #Envia tiempo que se ejecuto el AC
        self.socket.send(str(MAX_TIME).encode('utf-8'))

        #Envia estado inicial

        estadoEnvCifrado = (int(estadoEnvStr,2)) ^ self.numeroSecretoEnvio
        self.socket.send(estadoEnvCifrado.encode('utf-8')) 


        #Envia largo del texto cifrado
        self.socket.send(str(len(arregloCifrado)).encode('utf-8'))

        #Envia mensaje cifrado
        for i in arregloCifrado:
            self.socket.send(str(i).encode('utf-8'))
            sleep( 0.01 ) #TODO implementar una sincronización correcta

    def desconectarSaliente(self):
        self.socket.close()
