import os
from PIL import ImageTk, Image

class Images(object):
    def __init__(self):
        get_path = os.path.abspath(os.getcwd())
        self.background_1 = get_path + r"\Images\background1.png"
        self.background_2 = get_path + r"\Images\bitcoinimg.png"
        self.background_3 = get_path + r"\Images\darkbitcoin.png"
        self.exit = get_path + r"\Images\Exit.png"
        self.Login = get_path + r"\Images\Login.png"
        self.back = get_path + r"\Images\back.png"
        self.submit = get_path + r"\Images\submit.png"
        self.register = get_path + r"\Images\Register.png"

    def get_images(self):
        background_image_main = ImageTk.PhotoImage(Image.open(self.background_1))
        background_image_register = ImageTk.PhotoImage(Image.open(self.background_2))
        background_image_login = ImageTk.PhotoImage(Image.open(self.background_3))
        exit_button = ImageTk.PhotoImage(Image.open(self.exit))
        Login_button = ImageTk.PhotoImage(Image.open(self.Login))
        back_button = ImageTk.PhotoImage(Image.open(self.back))
        submit_button = ImageTk.PhotoImage(Image.open(self.submit))
        register_button = ImageTk.PhotoImage(Image.open(self.register).zoom(60, 100))
        return (background_image_main,background_image_register,exit_button,Login_button,back_button,submit_button,register_button)
    


