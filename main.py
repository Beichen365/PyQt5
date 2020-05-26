import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from UserManager import Ui

def main():
   app = QtWidgets.QApplication(sys.argv)
   window = Ui()
   window.show()
   app.exec_()

if __name__ == '__main__':
    main()