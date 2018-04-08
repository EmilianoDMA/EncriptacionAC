#!/usr/bin/python

#---------------------------------------------------------------------------------------#
#                                  CODIGO CIFRADOR                                      #
# EJECUTAR COMO: python AC.py <mensaje> <puerto>
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
from time import sleep

#Recibe el mensaje y lo pasa a un arreglo de int donde cada posicion es un caracter en su valor UTF-8
mensaje = sys.argv[1]
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
HOST = 'localhost'
PORT = 8081
#Envia tiempo que se ejecuto el AC
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(str(MAX_TIME).encode('utf-8'))
s.close()
#Envia estado inicial
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(estadoEnvStr.encode('utf-8')) 
#s.send(str(int(estadoEnvStr,2)).encode('utf-8'))
s.close()
#Envia largo del texto cifrado
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(str(len(arregloCifrado)).encode('utf-8'))
s.close()
#Envia mensaje cifrado
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
for i in arregloCifrado:
    s.send(str(i).encode('utf-8'))
    sleep( 0.01 ) #TODO implementar una sincronización correcta
s.close()
