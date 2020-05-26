import sys, mysql.connector
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence

from mydb import mydb


class DisplayResultsUI(QtWidgets.QMainWindow):
    def __init__(self, sql):
        super(DisplayResultsUI, self).__init__()
        uic.loadUi('UserManagerGUI/results.ui', self)

        self.shortcutBack = QShortcut(QKeySequence('Ctrl+B'),self)
        self.shortcutBack.activated.connect(self.goback)
        
 
        self.mydb = mydb()
        self.table = self.findChild(QtWidgets.QTableWidget, 'tablebox')
        self.back = self.findChild(QtWidgets.QPushButton, 'backbox')
        self.back.setToolTip('Ctrl + B')
        self.abanana = []
        self.statusbar = self.findChild(QtWidgets.QStatusBar, 'statusbar')

        self.mydb.dbcursor.execute(sql)
        myresult = self.mydb.dbcursor.fetchall()

        for x in myresult:
            self.abanana.append(x)

        for recordTuples in self.abanana:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            for i in range(len(recordTuples)):
                self.table.setItem(rowPosition, i, QTableWidgetItem(str(recordTuples[i])))
        
        self.statusbar.hide()
        self.back.clicked.connect(self.goback)

    def goback(self):
        self.hide()
        from UserManager import Ui
        self.ui = Ui()
        self.ui.show()
        self.close()