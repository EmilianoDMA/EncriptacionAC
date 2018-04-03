#!/usr/bin/python

#---------------------------------------------------------------------------------------#
#                                  CODIGO CIFRADOR                                      #
# --------------                                                                        #
# RECIBE: LA CADENA ORIGINAL                                                            #
# --------------                                                                        #
# GENERA UN ESTADO INICIAL ALEATORIO                                                    #
# EJECUTA EL AC CON ESE ESTADO INICIAL POR UN X TIEMPO HASTA LLEGAR A UN ESTADO FINAL   #
# ENCRIPTA EL MENSAJE USANDO EL ESTADO FINAL COMO MASCARA                               #
# --------------                                                                        #
# ENVIA: MENSAJE ENCRIPTADO, ESTADO INICIAL (Diffie-Hellman), TIEMPO X                  #
#---------------------------------------------------------------------------------------#

import sys
import random
import binascii
import socket
from pdb import set_trace

#Recibe el mensaje y lo pasa a bytes
mensaje = sys.argv[1]
mensajeUTF = list (mensaje.encode('utf-8'))
print("Mensaje:", mensaje)
print("Mensaje UTF:", mensajeUTF)

MAX_TIME = len(mensaje) * 8
HALF_SIZE = MAX_TIME
indices = range(-HALF_SIZE, HALF_SIZE+1)

#Genera un estado inicial en Cells para el AC
cells = {i: '0' for i in indices}
for i in cells:
    azar = random.randint(0,1)
    cells[i] = str(azar)        
cells[-HALF_SIZE-1] = '0' # Llena ambos extremos
cells[ HALF_SIZE+1] = '0'
estadoInicial = []
estadoInicial = cells #Guarda el estado inicial

#Ejecuta el AC y genera la mascara a partir del estado final
new_state = {"111": '0', "110": '0', "101": '0', "000": '0',
             "100": '1', "011": '1', "010": '1', "001": '1'} #Comportamiento que tendrá
for time in range(0, MAX_TIME): #Ejecucion
    patterns = {i: cells[i-1] + cells[i] + cells[i+1] for i in
                indices}
    cells = {i: new_state[patterns[i]] for i in indices}
    cells[-HALF_SIZE-1] = '0'
    cells[ HALF_SIZE+1] = '0'

#Creación de la máscara a partir del último estado del AC
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


#CIFRADO. Se cifra haciendo un XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje (en binario).
arregloCifrado = []
indice = 0
for m in mensajeUTF:
    arregloCifrado.append((m ^ mascara[indice]))
    indice = indice + 1 
#print(textoCifrado) #TEXTO CIFRADO A ENVIAR

#toma el estado inicial y lo parsea a Str para que sea más facil la interpretación luego, del lado del decifrador.
estadoEnv = []
for i in estadoInicial:
    estadoEnv.append(estadoInicial[i])
estadoEnvStr = ''.join(estadoEnv)

#Enviar estadoInicial, textoCifrado, MAX_TIME
print("Estado Inicial: ", estadoEnvStr)
print("Tiempo: ", MAX_TIME)
print("Mensaje cifrado: ", arregloCifrado)

# MANDA mandar
HOST = 'localhost'
PORT = 8081
#Envia estado inicial
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(sys.argv[2]))) #argv2 es el puerto
s.send(estadoEnvStr.encode('utf-8'))
s.close()
#Envia tiempo
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(sys.argv[2]))) #argv2 es el puerto
s.send(str(MAX_TIME).encode('utf-8'))
s.close()
#Envia largo del cifrado
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(sys.argv[2]))) #argv2 es el puerto
s.send(str(len(arregloCifrado)).encode('utf-8'))
s.close()
#Envia mensaje cifrado
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(sys.argv[2]))) #argv2 es el puerto
for i in arregloCifrado:
    s.send(str(i).encode('utf-8'))
    print(str(i).encode('utf-8')) #TODO meter un sleep en vez de esta linea o algun tipo de sincronización
s.close()
