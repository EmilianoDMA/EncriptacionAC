import sys
from PyQt5 import QtWidgets

from Vista.Vista import Vista
from Vista.DialogoConexion import DialogoConexion

if __name__ == '__main__':
    pass  # TODO Hacer algo acá
    app = QtWidgets.QApplication(sys.argv)
    ex = Vista()
    ex1 = DialogoConexion(ex)
    sys.exit(app.exec_())
