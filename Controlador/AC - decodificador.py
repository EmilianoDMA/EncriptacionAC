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

#Recibe el mensaje encriptado en string binario
mensajeCifrado = sys.argv[1]

#Setea el tiempo recibido y otras variables
MAX_TIME = int(sys.argv[3])
HALF_SIZE = MAX_TIME
indices = range(-HALF_SIZE, HALF_SIZE+1)

#Recibe el estado inicial del ACl
cellsRecv = sys.argv[2]

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
mascara = [] #Creación de la máscara a partir del último estado del AC
for i in indices: #el estado del AC está en char. Por esto se recorre el mismo y se appendea en mascara[] el equivalente en integer de cada posición.
    if cells[i] == '1': #cells[] contiene el último estado del AC
        mascara.append(1)
    else:
        mascara.append(0)

#convierte el string recivido a un arreglo de enteros binarios para poder hacer el XOR
arregloCifrado = list(mensajeCifrado) #convierte el string a array
arregloCifradoInt = [] #convierte el arreglo de char en arreglo de int
for i in arregloCifrado:
    arregloCifradoInt.append(int(i))

#DESCIFRADO. Se descifra haciendo un XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje cifrado (en binario). Se obtiene el binario original.
arregloDescifrado = []
indice = 0
for m in arregloCifradoInt:
    arregloDescifrado.append(str(m ^ mascara[indice]))
    indice = indice + 1
textoDescifradoBin = ''.join(arregloDescifrado) #Se hace un join del arreglo para que este quede en forma de cadena. Está expresado en binario.


#TODO convertir el binario en texto teniendo en cuenta la longitud (tiempo / 4) de la cadena original.
print(arregloDescifrado)

arregloDividido = []
concat = ""
bitCant = 1
for n in arregloDescifrado:
    concat =  concat + n
    if bitCant == 4:
        arregloDividido.append(concat)
        bitCant = 0
        concat = ""
    bitCant = bitCant + 1
print(arregloDividido)
    


print(textoDescifradoBin)

