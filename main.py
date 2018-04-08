import sys
from PyQt5 import QtWidgets

from Vista.Vista import Vista

if __name__ == '__main__':
    pass  # TODO Hacer algo acá
    app = QtWidgets.QApplication(sys.argv)
    ex = Vista()
    sys.exit(app.exec_())
