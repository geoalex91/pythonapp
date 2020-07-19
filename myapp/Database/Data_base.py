import sqlite3 as db
import os
class database():
    def __init__(self, **kwargs):
        self.filename = kwargs.get("filename")
        self.table = kwargs.get("table","users")
        
    def sql_do(self, sql, *params):
        self._mydb.execute(sql, params)
        self._mydb.commit()
        
    def create_table(self, name, parameter1, parameter2):
        self._appcursor.execute("CREATE TABLE {} ({} text, {} text)".format(name, parameter1, parameter2))
        self._mydb.commit()

    def close(self):
        self._mydb.close()

    def insert_register(self, values):
        self._appcursor.execute("INSERT INTO {} (user, password) VALUES (?, ?)".format(self._table) ,(values["user"],values["password"]))
        self._mydb.commit()

    def insert(self, column, values):
        self._appcursor.execute("INSERT INTO {} ({}) VALUES (?)".format(self._table, column) ,(values[column],))
        self._mydb.commit()

    def update(self,column, newvalue):
        self._appcursor.execute("UPDATE {} set {} = {}".format(self._table, column, newvalue))
        self._mydb.commit()

    def get_password(self, values):
        try:
            result = None
            self._appcursor.execute("SELECT password from {} WHERE user = '{}'".format(self._table,values))
            result = self._appcursor.fetchone()
            return result[0]
        except:
            print("No username available")

    @property
    def filename(self):
        return self._filename
    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._mydb = db.connect(fn)
        self._mydb.row_factory = db.Row
        self._appcursor = self._mydb.cursor()

    @filename.deleter
    def filename(self):
        self.close()

    @property
    def table(self):
        return self._table
    @table.setter
    def table(self, t):
        self._table = t
    @table.deleter
    def table(self):
        del self._table

    def close(self):
        self._mydb.close()
        del self._filename
