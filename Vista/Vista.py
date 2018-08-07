import socket
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from Vista.UI import Ventana, ConexionDialog
from Controlador.Controlador import Controlador

class Vista(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.controlador = Controlador(self)
        self.controlador.recibir_mensaje.connect(self.escribirMensajeRecibido)
        self.controlador.fin_dh.connect(self.habilitarVista)
        self.ventana = Ventana.Ui_MainWindow()
        self.ventana.setupUi(self)
        self.inicializaUI()
        self.show()

    def inicializaUI(self):
        self.setWindowTitle('EncripChat v7.11.501-r272')
        self.ventana.mensajes.setReadOnly(True)
        self.ventana.enviar.clicked.connect(self.controlador.enviarMensaje)
        self.ventana.actionConectar.triggered.connect(self.conectar)
        self.ventana.actionDesconectar.triggered.connect(self.cerrarConexiones)
        self.ventana.actionSalir.triggered.connect(self.salir)

    def deshabilitarVista(self):
        self.ventana.escribir.setReadOnly(True)
        self.ventana.enviar.setEnabled(False)
        self.ventana.menuOpciones.setEnabled(False)

    @QtCore.pyqtSlot()
    def habilitarVista(self):
        self.ventana.escribir.setReadOnly(False)
        self.ventana.enviar.setEnabled(True)
        self.ventana.menuOpciones.setEnabled(True)

    def getContenidoMensaje(self):
        mensaje = self.ventana.escribir.toPlainText()
        self.ventana.escribir.clear()
        return mensaje

    @QtCore.pyqtSlot(str)
    def escribirMensajeRecibido(self, mensaje):
        contenido = self.ventana.mensajes.toPlainText()
        self.ventana.mensajes.clear()
        self.ventana.mensajes.setPlainText(contenido+">>>"+mensaje+"\n")

    def escribirMensajeEnviado(self, mensaje):
        contenido = self.ventana.mensajes.toPlainText()
        self.ventana.mensajes.clear()
        self.ventana.mensajes.setPlainText(contenido+">"+mensaje+"\n")

    def limpiarMensajes(self):
        self.ventana.mensajes.clear()

    def informarError(self, error):
        self.ventana.mensajes.clear()
        self.ventana.mensajes.setPlainText(error)

    def enviarMensaje(self):
        self.ventana.escribir.cut()
        self.controlador.enviarMensaje()

    def obtenerPuerto(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Pedimos al servidor un puerto libre
        sock.connect((ip, 9000))
        sock.send('conn'.encode())
        puerto = sock.recv(1024)
        # TODO Validar que el puerto sea valido
        print(puerto)
        sock.close()

        return int(puerto.decode())

    def conectar(self, ip):
        self.controlador.conectar(ip, self.obtenerPuerto(ip))
        #self.habilitarVista()

    def cerrarConexiones(self):
        self.controlador.desconectar()

    def salir(self):
        self.cerrarConexiones()
        self.close()
