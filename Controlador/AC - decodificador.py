#!/usr/bin/python

#---------------------------------------------------------------------------------------#
#                                  CODIGO DESCIFRADOR                                   #
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

# RECIBE computar
HOST = 'localhost'
PORT = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, int(sys.argv[1])))
#Recibe estado inicial
s.listen(1)
conn, addr = s.accept()
cellsRecv = conn.recv(1024).decode('utf-8')
print("Estado Inicial: ", cellsRecv)
conn.close()
#Recibe tiempo
s.listen(1)
conn, addr = s.accept()
MAX_TIME = int(conn.recv(1024).decode('utf-8'))
print("Tiempo: ", MAX_TIME)
conn.close()
#Recibe el largo del mensaje
s.listen(1)
conn, addr = s.accept()
maxLoop = int(conn.recv(1024).decode('utf-8'))
print("Largo: ", maxLoop)
conn.close()
#Recibe el mensaje encriptado
mensajeCifrado = []
s.listen(1)
conn, addr = s.accept()
for x in range(0, maxLoop):
    aux = int(conn.recv(1024).decode('utf-8'))
    mensajeCifrado.append(aux)
conn.close()
print("Mensaje cifrado: ", mensajeCifrado)

#Setea el tiempo recibido y otras variables
HALF_SIZE = MAX_TIME
indices = range(-HALF_SIZE, HALF_SIZE+1)

#Genera un estado inicial en Cells para el AC
cells = {i: '0' for i in indices}
cont = 0
for i in cells:
    valor = cellsRecv[cont]
    cont = cont + 1
    cells[i] = str(valor)
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


#Pasa la mascara a decimal
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

#convierte el string recivido a un arreglo de enteros binarios para poder hacer el XOR
arregloCifrado = list(mensajeCifrado) #convierte el string a array
arregloCifradoInt = [] #convierte el arreglo de char en arreglo de int
for i in arregloCifrado:
    arregloCifradoInt.append(int(i))

#DESCIFRADO. Se descifra haciendo un XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje cifrado (en binario). Se obtiene el binario original.
arregloDescifrado = []
indice = 0
for m in arregloCifradoInt:
    arregloDescifrado.append((m ^ mascara[indice]))
    indice = indice + 1

#TODO convertir el binario en texto teniendo en cuenta la longitud (tiempo / 4) de la cadena original.
print("Mensaje UTF: ", arregloDescifrado)
cadena = bytes(arregloDescifrado)
textoDescifrado = cadena.decode('utf-8')
print(textoDescifrado)