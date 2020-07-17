import sqlite3 as db
import os
class database():
    def __init__(self):
        path = os.path.abspath(os.getcwd())
        databasefile = path + r"\Database\appdatabase.db"
        self.mydb = db.connect(databasefile)
        self.appcursor = self.mydb.cursor()
        
    def create_table(self, name, parameter1, parameter2):
        self.appcursor.execute("CREATE TABLE {} ({} text, {} text)".format(name, parameter1, parameter2))
        self.mydb.commit()
    def close(self):
        self.mydb.close()

    def insert_register(self, table, values):
        self.appcursor.execute("INSERT INTO {} (user, password) VALUES (?, ?)".format(table) ,(values["user"],values["password"]))
        self.mydb.commit()

