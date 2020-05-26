import sys, mysql.connector
from mysql.connector import Error

class mydb():
    def __init__(self):        
        self.dbconnection = mysql.connector.connect(
                          host="localhost",
                          user="testuser",
                          database="testdb"
                        )
        self.dbcursor = self.dbconnection.cursor()