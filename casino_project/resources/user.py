from database.Data_base import Database
import os
abs_path = os.path.abspath(os.getcwd())
class User(object):
    _database_file = abs_path + r".\database\appdatabase.db"
    def __init__(self,**kwargs):
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self._dat = Database(filename = User._database_file, table = "users")

    def __del__(self):
        self._dat.close()
        self._username = None
        self._password = None

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self,us):
        self._username = us

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, pw):
        self._password = pw
    
    def login(self):
        if self._dat.get_record("password", self._username) == self._password:
            return True
        else:
            return False

    def register(self, name, photo):
        with open(photo, 'rb') as pic:
            blob = pic.read()
            base = os.path.basename(photo)
            pic_name, ext = os.path.splitext(base)
            self._dat.insert_register(dict(user = self._username, password = self._password, name = name, photo = blob, photo_ext = ext, photo_name = pic_name, cash = 1000))
    def search_username(self, username):
        self._dat.sql_do("""CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY, user text, password text, name text, photo blob,photo_ext text, photo_name text, cash integer)""")
        if self._dat.get_record("user", username) is not None:
            return False
        else:
            return True
    def get_profile_pic(self):
        blob, ext, pic_name = self._dat.get_multiple_records(self._username)
        filename = pic_name + ext
        output_file = open(filename, 'wb')
        output_file.write(blob)
        return filename

    def update_profile_pic(self, photo):
        with open(photo, 'rb') as pic:
            blob = pic.read()
            base = os.path.basename(photo)
            pic_name, ext = os.path.splitext(base)
            self._dat.update_photo(dict(photo = blob, user = self._username))
            self._dat.update("photo_ext", dict(photo_ext = ext, user = self._username))
            self._dat.update("photo_name", dict(photo_name = pic_name, user = self._username))

    def set_name(self, new_name):
        self._dat.update("name", dict(name = new_name, user = self._username))
    def get_name(self):
        name = self._dat.get_record("name", self._username)
        return name
    def set_password(self, new_password):
        self._dat.update("password", dict(password = new_password, user = self._username))
    
    def get_money(self):
        money = self._dat.get_record("cash", self._username)
        return money
    def set_money(self, new_value):
        self._dat.update("cash", dict(cash = new_value, user = self._username))
class Admin(User):
    pass
