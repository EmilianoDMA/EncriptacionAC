#!/usr/bin/python

#---------------------------------------------------------------------------------------#
#                                  CODIGO DESCIFRADOR                                   #
# EJECUTAR COMO: "AC - decodificador.py" <puerto>                                       #
# --------------                                                                        #
# RECIBE: CADENA ENCRIPTADA, ESTADO INICIAL, TIEMPO X                                   #
# --------------                                                                        #
# EJECUTA EL AC CON EL ESTADO INICIAL POR EL TIEMPO X HASTA LLEGAR AL ESTADO FINAL      #
# DESENCRIPTA EL MENSAJE USANDO EL ESTADO FINAL COMO MASCARA                            #
# --------------                                                                        #
# ENVIA: MENSAJE ORIGINAL                                                               #
#---------------------------------------------------------------------------------------#

import sys
import random
import binascii
import socket
from pdb import set_trace

#RECEPCIÓN. Setea la conexión y recibe los datos necesarios
HOST = 'localhost'
PORT = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
#Recibe tiempo que se ejecutará el AC
s.listen(1)
conn, addr = s.accept()
MAX_TIME = int(conn.recv(1024).decode('utf-8'))
conn.close()
#Recibe estado inicial
s.listen(1)
conn, addr = s.accept()
cellsRecv = conn.recv((MAX_TIME * 2)+1).decode('utf-8')
conn.close()
#Recibe el largo del mensaje encriptado
s.listen(1)
conn, addr = s.accept()
maxLoop = int(conn.recv(1024).decode('utf-8'))
conn.close()
#Recibe el mensaje encriptado
mensajeCifrado = []
s.listen(1)
conn, addr = s.accept()
for x in range(0, maxLoop):
    aux = int(conn.recv(1024).decode('utf-8'))
    mensajeCifrado.append(aux)
conn.close()

#Setea el tiempo recibido y otras variables
HALF_SIZE = MAX_TIME
indices = range(-HALF_SIZE, HALF_SIZE+1)
#Setea el estado inicial recibido para ejecutar el AC
cells = {i: '0' for i in indices}
cont = 0
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
print(textoDescifrado)
