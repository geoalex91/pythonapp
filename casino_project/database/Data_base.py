import sqlite3 as db
import os
class Database():
    def __init__(self, **kwargs):
        self.filename = kwargs.get("filename")
        self.table = kwargs.get("table","users")
        
    def sql_do(self, sql, *params):
        self._mydb.execute(sql, params)
        self._mydb.commit()
        
    def create_table(self, name, **kwargs):
        self._appcursor.execute("CREATE TABLE IF NOT EXISTS {} ({} {})".format(name, kwargs, kwargs.values()))
        self._mydb.commit()

    def close(self):
        self._mydb.close()

    def insert_register(self, values):
        self._appcursor.execute("INSERT INTO {} (user, password, name, photo, photo_ext, photo_name, cash) VALUES (?, ?, ?, ?, ?, ?, ?)".format(self._table) ,
            (values["user"],values["password"], values["name"],db.Binary(values["photo"]),values["photo_ext"],values["photo_name"],values["cash"]))
        self._mydb.commit()

    def insert(self, **kwargs):
        self._appcursor.execute("""INSERT INTO {} ({}) VALUES ({})""".format(self._table,list(kwargs.keys()), list(kwargs.values())))

    def update(self,column, values):
        self._appcursor.execute("UPDATE {} set {} = ? where user = ?".format(self._table, column), (values[column], values["user"]))
        self._mydb.commit()
    def update_photo(self, values):
        self._appcursor.execute("""Update {} set photo = ? where user = ?""".format(self._table), (db.Binary(values["photo"]), values["user"]))
        self._mydb.commit()
    def get_record(self,value1, value2):
        try:
            #print(value2)
            result = "None"
            self._appcursor.execute("SELECT {} from {} WHERE user = '{}'".format(value1,self._table,value2))
            result = self._appcursor.fetchone()
            return dict(result)[value1]
        except:
            print("No username available")

    def get_multiple_records(self,value):
        try:
            #print("val2 " + value)
            result = "None"
            self._appcursor.execute("SELECT photo, photo_ext, photo_name from {} WHERE user = '{}'".format(self._table,value))
            result = self._appcursor.fetchone()
            print (result)
            return dict(result).values()
        except:
            print("No username available")
    @property
    def filename(self):
        return self._filename
    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._mydb = db.connect(fn, check_same_thread= False)
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
