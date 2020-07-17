from tkinter import *
from tkinter import messagebox
from Database.Data_base import database
from images.Images import Images
import os
from PIL import ImageTk, Image

class app(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #=========program config=============
        self.title("Bitcoin machine")
        self.geometry("600x600")
        self.config(bg = "black")
        logo_path = os.path.abspath(os.getcwd())
        logo_image = logo_path + r"\Images\bclogo.png"
        self.iconphoto(False, PhotoImage(file = logo_image))
        #=======================================
        main_frame = Frame(self)
        main_frame.place(relwidth = 0.9, relheight = 0.9, relx = 0.05, rely = 0.05)
        
        self.frames = {}
        for F in (main_window,Register_window,Login_window,Profile_window):
            frame = F(main_frame,self)
            self.frames[F] = frame
            frame.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)

        self.show_frame(main_window)
    def show_frame(self,window):
        frame = self.frames[window]
        frame.tkraise()

class main_window(Frame):
    def __init__(self, parent,controller):
        Frame.__init__(self,parent)
        #============background=================
        self.config(bg = "red")
        img = Images()
        self.background_image = img.get_images()[0]
        backgr_img = Canvas(self,width = 500, height = 500, bg = "black")
        backgr_img.create_image(250,280, image = self.background_image)
        backgr_img.create_text(160,50,text = "Bitcoin app.\nRegister and earn some money", fill = "white")
        backgr_img.place(relheight = 1.25, relwidth = 1.2, relx = -0.1, rely = -0.01)
        #==============Buttons===========
        self.regbtn = img.get_images()[6]
        Register_button = Button(backgr_img, height = 60,width = 100, command=lambda:controller.show_frame(Register_window),image = self.regbtn)
        Register_button.place(relx = 0.7, rely = 0.1)
        Login_button = Button(backgr_img, text = "  Login ", padx = 30, pady = 20, command = lambda:controller.show_frame(Login_window))
        Login_button.place(relx = 0.7, rely = 0.22)
        Exit_button = Button(backgr_img, text = "   Exit   ",padx = 30, pady = 20, command = controller.quit)
        Exit_button.place(relx = 0.7, rely = 0.34)
		

class Register_window(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #===========background================
        self.config(bg = "red")
        self.background_image = ImageTk.PhotoImage(Image.open(r"C:\Users\george\source\repos\myapp\myapp\images\background1.png"))
        self.backgr_img = Canvas(self,width = 500, height = 500, bg = "black")
        self.backgr_img.create_image(250,280, image = self.background_image)
        self.backgr_img.create_text(300,50,text = "Register form", fill = "white", font =("Arial", 18))
        self.backgr_img.create_text(270,145,text = "Username", fill = "white")
        self.backgr_img.create_text(270,170,text = "Password", fill = "white")
        self.backgr_img.create_text(270,195,text = "Retype Password", fill = "white")
        self.backgr_img.place(relheight = 1.25, relwidth = 1.2, relx = -0.1, rely = -0.01)
        #============User input====================
        self.username_e = Entry(self.backgr_img)
        self.username_e.place(relx = 0.5, rely = 0.2)
        self.username_e.insert(0,"Enter a username")
        self.password_e = Entry(self.backgr_img)
        self.password_e.place(relx = 0.5, rely = 0.24)
        self.password_e.insert(0,"Enter a password")
        self.passwordr_e = Entry(self.backgr_img)
        self.passwordr_e.place(relx = 0.5, rely = 0.28)
        self.passwordr_e.insert(0,"Reenter a your password")
        #=============Buttons================
        Goback = Button(self, text="Go back", command=lambda:[controller.show_frame(main_window),self.delete_text(txtshow)], padx = 15, pady = 10)
        Goback.place(relx = 0.35, rely = 0.45)
        submit_button = Button(self, text="Submit ", padx = 15, pady = 10, command = self.submit)
        submit_button.place(relx = 0.58, rely = 0.45)

    def submit(self):
        if (not self.username_e.get()) or (not self.password_e.get()):
            messagebox.showinfo("Error","You did not entered a username or a password")
        elif (" " in self.username_e.get()) or (" " in self.password_e.get()):
            messagebox.showinfo("Error","this should not contain spaces")
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
        elif len(self.password_e.get()) < 5:
            messagebox.showinfo("Error","Password length must be more than five")
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
        elif len(self.username_e.get()) < 5:
            messagebox.showinfo("Error","Username length must be more than five")
            self.username_e.delete(0, END)
        elif self.password_e.get() != self.passwordr_e.get():
            messagebox.showinfo("Error","password not matching")
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
        else:
            dat = database()
            dat.insert_register("users",dict(user = self.username_e.get(), password = self.password_e.get()))
            dat.close()
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
            global txtshow
            txtshow = self.backgr_img.create_text(230,250,text = "you successfuly made an account", fill = "white")

    def delete_text(self,text):
                self.backgr_img.delete(text)
        
class Login_window(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        #===========Background===========
        self.config(bg = "red")
        self.background_image = ImageTk.PhotoImage(Image.open(r"C:\Users\george\source\repos\myapp\myapp\images\background1.png"))
        backgr_img = Canvas(self,width = 500, height = 500, bg = "black")
        backgr_img.create_image(250,280, image = self.background_image)
        backgr_img.create_text(300,50,text = "Login", fill = "white", font =("Arial", 18))
        backgr_img.create_text(270,145,text = "Username", fill = "white")
        backgr_img.create_text(270,170,text = "Password", fill = "white")
        backgr_img.place(relheight = 1.25, relwidth = 1.2, relx = -0.1, rely = -0.01)
        #============User input====================
        username_e = Entry(backgr_img)
        username_e.place(relx = 0.5, rely = 0.2)
        username_e.insert(0,"Enter a username")
        password_e = Entry(backgr_img)
        password_e.place(relx = 0.5, rely = 0.24)
        password_e.insert(0,"Enter a password")
        #=============Buttons================
        Goback = Button(self, text="Go back", command=lambda:controller.show_frame(main_window), padx = 15, pady = 10)
        Goback.place(relx = 0.35, rely = 0.45)
        submit_button = Button(self, text="Submit ", padx = 15, pady = 10)
        submit_button.place(relx = 0.58, rely = 0.45)

class Profile_window(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        #===========Background===========
        self.config(bg = "red")
        self.background_image = ImageTk.PhotoImage(Image.open(r"C:\Users\george\source\repos\myapp\myapp\images\background1.png"))
        backgr_img = Canvas(self,width = 500, height = 500, bg = "black")
        backgr_img.create_image(250,280, image = self.background_image)
        backgr_img.place(relheight = 1.25, relwidth = 1.2, relx = -0.1, rely = -0.01)
app_core = app()
app_core.mainloop()