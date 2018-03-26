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

#Recibe el mensaje y lo pasa a bytes
mensaje = sys.argv[1]
mensajeUTF = mensaje.encode('utf-8')
msjBytes = bytes(mensajeUTF)

MAX_TIME = len(mensaje) * 4
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
mascara = [] #Creación de la máscara a partir del último estado del AC
for i in indices: #el estado del AC está en char. Por esto se recorre el mismo y se appendea en mascara[] el equivalente en integer de cada posición.
    if cells[i] == '1': #cells[] contiene el último estado del AC
        mascara.append(1)
    else:
        mascara.append(0)

#Pasa el mensaje de Bytes a su equivalente binario en un arreglo de enteros de la forma [1, 0, 0, 0, 1, 0, 1,......]
msjBinario = []
count = 0
for j in msjBytes:
    binario = bin(j) #pasa cada byte a su equivalente binario en forma de "0bxxxxxxxx"
    for k in binario: #recorre el byte en binario con un contador para omitir el "0b" de cada byte.
        if count > 1:
            msjBinario.append(int(k)) #appendea solo la parte binaria posterior a "0b" de cada byte en msjBinario. Cada bit lo appendea individualmente.
        count = count + 1
    count = 0
print("BINARIO")
print(msjBinario)
#CIFRADO. Se cifra haciendo un XOR elemento a elemento entre la mascara (último estado del AC) y el mensaje (en binario).
arregloCifrado = []
indice = 0
for m in msjBinario:
    arregloCifrado.append(str(m ^ mascara[indice]))
    indice = indice + 1
textoCifrado = ''.join(arregloCifrado) #Se hace un join del arreglo para que este quede en forma de cadena.
#print(textoCifrado) #TEXTO CIFRADO A ENVIAR

#toma el estado inicial y lo parsea a Str para que sea más facil la interpretación luego, del lado del decifrador.
estadoEnv = []
for i in estadoInicial:
    estadoEnv.append(estadoInicial[i])
estadoEnvStr = ''.join(estadoEnv)

#Enviar estadoInicial, textoCifrado, MAX_TIME
print(textoCifrado)
print(estadoEnvStr)
print(MAX_TIME)