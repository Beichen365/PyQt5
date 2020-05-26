import sys, mysql.connector
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from mydb import mydb
from SearchUser import DisplayResultsUI

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        
        uic.loadUi('UserManagerGUI/saveuserGUI.ui', self)

        self.shortcutSave = QShortcut(QKeySequence('Ctrl+S'),self)
        self.shortcutSave.activated.connect(self.saveuser)
        self.shortcutSearch = QShortcut(QKeySequence('Ctrl+E'),self)
        self.shortcutSearch.activated.connect(self.searchuser)

        self.mydb = mydb()
        
        self.edited = False  
        self.statusbar = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        self.name = self.findChild(QtWidgets.QTextEdit, 'namebox')
        self.age = self.findChild(QtWidgets.QTextEdit, 'agebox')
        self.gender = self.findChild(QtWidgets.QComboBox, 'genderbox')
        self.phone = self.findChild(QtWidgets.QTextEdit, 'phonenumberbox')
        self.role = self.findChild(QtWidgets.QComboBox, 'rolebox')
        self.address = self.findChild(QtWidgets.QTextEdit, 'addressbox')
        self.save = self.findChild(QtWidgets.QPushButton, 'savebox')
        self.search = self.findChild(QtWidgets.QPushButton, 'searchbox')
        self.lastfive = self.findChild(QtWidgets.QTableWidget, 'lastfivebox')
        self.delete = self.findChild(QtWidgets.QPushButton, 'deletebox')
        self.check1 = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.check2 = self.findChild(QtWidgets.QCheckBox, 'checkBox_2')
        self.check3 = self.findChild(QtWidgets.QCheckBox, 'checkBox_3')
        self.check4 = self.findChild(QtWidgets.QCheckBox, 'checkBox_4')
        self.check5 = self.findChild(QtWidgets.QCheckBox, 'checkBox_5')

        self.save.setToolTip('Ctrl + S')
        self.search.setToolTip('Ctrl + E')
        
        self.name.setFocus()
        tabSeq = self.setTabOrder
        tabSeq(self.name, self.save)
        tabSeq(self.save, self.search)
        tabSeq(self.search, self.address)
        tabSeq(self.address, self.role)
        tabSeq(self.role, self.phone)
        tabSeq(self.phone, self.gender)
        tabSeq(self.gender, self.age)
        tabSeq(self.age, self.name)
        
        self.DisplayLastFive()
        self.statusbar.hide()

        self.save.clicked.connect(self.saveuser)
        self.search.clicked.connect(self.searchuser)
        self.delete.clicked.connect(self.deleteLine)
        self.lastfive.cellDoubleClicked.connect(self.editRow)

        self.show()
        
    
    def DisplayLastFive(self):
        self.lastfive.setRowCount(0);

        phrase = "SELECT * FROM Users ORDER BY id DESC LIMIT 5 ;"

        self.mydb.dbcursor.execute(phrase)
        self.listOfTuples = self.mydb.dbcursor.fetchall()
        for mytuple in self.listOfTuples:
            rowPosition = self.lastfive.rowCount()
            self.lastfive.insertRow(rowPosition)
            checkbox = QCheckBox()
            self.lastfive.setCellWidget(rowPosition,0,checkbox)
            for j in range(len(mytuple)):
                self.lastfive.setItem(rowPosition, j + 1, QTableWidgetItem(str(mytuple[j])))
        self.lastfive.resizeColumnToContents(0)
        return
    
    def deleteLine(self):
        self.mydb.dbcursor.execute("SET SQL_SAFE_UPDATES=0;")
        for selected in range(len(self.listOfTuples)):        
            if self.lastfive.cellWidget(selected,0).isChecked():
                id = self.listOfTuples[selected][6]
                self.mydb.dbcursor.execute("DELETE FROM Users WHERE id = "+str(id)+";")
                self.mydb.dbconnection.commit()

        self.DisplayLastFive()

    def editRow(self, row, column):
        self.selectedID = self.listOfTuples[row][6]
        self.name.setText(self.lastfive.item(row,1).text())
        self.age.setText(self.lastfive.item(row,2).text())
        self.gender.setCurrentText(self.lastfive.item(row,3).text())
        self.phone.setText(self.lastfive.item(row,4).text())
        self.role.setCurrentText(self.lastfive.item(row,5).text())
        self.address.setText(self.lastfive.item(row,6).text())
        self.edited = True

    def saveuser(self):
        try:
            
            if self.edited == True:
                self.mydb.dbcursor.execute("SET SQL_SAFE_UPDATES=0;")
                self.mydb.dbcursor.execute("DELETE FROM Users WHERE id = "+str(self.selectedID)+";")
                self.mydb.dbconnection.commit()
                self.edited = False
                
            sqlCommand = "SELECT * FROM Users WHERE name LIKE" + "'" +  self.name.toPlainText() + "';"
            
            self.mydb.dbcursor.execute(sqlCommand) 
            myresultSelected = self.mydb.dbcursor.fetchall()
            val = (self.name.toPlainText(), self.age.toPlainText(), self.gender.currentText(), self.phone.toPlainText(), self.role.currentText(), self.address.toPlainText())
            for a in myresultSelected:
                if a[0] == val[0] and a[3] == val[3]:
                    msgSaved = QMessageBox()
                    msgSaved.setIcon(QMessageBox.Information)

                    msgSaved.setText("!")
                    msgSaved.setInformativeText("The information was already saved before")
                    msgSaved.setWindowTitle("")

                    msgSaved.setStandardButtons(QMessageBox.Ok)
                    msgSaved.show()        
                    msgSaved.exec_()
                    return
                    
            sql = "INSERT INTO Users (name, age, gender,phoneNum,role,address) VALUES (%s, %s, %s, %s, %s, %s);"
                
            self.mydb.dbcursor.execute(sql,val)
            self.mydb.dbconnection.commit() 
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Done!")
            msg.setInformativeText("The information has been saved")
            msg.setWindowTitle("")

            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()        
            msg.exec_()
            
            self.comboData = []
            self.DisplayLastFive()
            self.name.clear()
            self.age.clear()
            self.phone.clear()
            self.address.clear()

            for stuffinCombo in range(self.gender.count()):
                self.comboData.append(self.gender.itemText(stuffinCombo))
            self.gender.clear()
            self.gender.addItems(self.comboData)

            self.comboData = []
            for stuffinCombo in range(self.role.count()):
                self.comboData.append(self.role.itemText(stuffinCombo))
            self.role.clear()
            self.role.addItems(self.comboData)


                

            
            

            
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("There is an error")
            msg.setInformativeText("Make sure you entered something for every box")
            msg.setWindowTitle("")

            msg.setStandardButtons(QMessageBox.Ok)
           
            msg.show()
            msg.exec_()
            
                        
    def searchuser(self):
        self.hide()
        sql = "SELECT * FROM Users WHERE name LIKE " + "'%" + self.name.toPlainText() + "%'"+" AND age LIKE '"+self.age.toPlainText()+"%'"+" AND gender LIKE '"+str(self.gender.currentText())+"%' AND phoneNum LIKE '"+self.phone.toPlainText()+"%'"+" AND role LIKE '%"+str(self.role.currentText())+"' AND address LIKE "+"'%"+self.address.toPlainText()+"%' ORDER BY id DESC"+ ";"

        sys.path.append(".")

        self.ui2 = DisplayResultsUI(sql)
        self.ui2.show()
        self.close()
        
        
        

    



    



