from tkinter import *
from tkinter import messagebox
import os
from PIL import ImageTk, Image, ImageDraw, ImageFilter
from database.Data_base import Database
from resources.user import User
from singleton_decorator import singleton
from tkinter import filedialog
from resources.games import Roulette, Balance, BlackJack, Bet
#=============PATHS==============
abs_path = os.path.abspath(os.getcwd())
logo_image_path = abs_path + r"\images\bclogo.png"
background_image_path = abs_path + r"\images\darkbitcoin.png"
Exit_image_path = abs_path + r"\images\Exit.png"
Login_image_path = abs_path + r"\images\Login.png"
Register_image_path = abs_path + r"\images\Register.png"
Back_image_path = abs_path + r"\images\back.png"
Submit_image_path = abs_path + r"\images\submit.png"
Login_bg_path =abs_path + r"\images\bitcoinimg.png"
profile_image = abs_path + r"\images\profile.png"
home_logo_path = abs_path + r"\images\homelogo.png"
databasefile = abs_path + r"\database\appdatabase.db"

class App(Tk):
    _profile_name = ""
    profile_img = profile_image
    def __init__(self):
        Tk.__init__(self)
        self.title("Crypto Casino")
        self.geometry("800x600")
        self.iconphoto(False,PhotoImage(file = logo_image_path))
        self.upper_frame = Frame(self, height = 70, width = 20, bg = "black")
        self.upper_frame.pack(fill='both')
        #===========CANVAS============
        self.show_profile_pic(App.profile_img)
        self.logo_img = ImageTk.PhotoImage(Image.open(home_logo_path).resize((60,60), Image.ANTIALIAS))
        self.home = Canvas(self.upper_frame, height = 60, width = 60, highlightthickness=0, bd =0, bg = 'black')
        self.home.place(x = 20, y = 5)
        self.home_logo_img = self.home.create_image(0,0, image = self.logo_img, anchor = NW)
        self.home.tag_bind(self.home_logo_img,'<ButtonPress - 1>', self.go_home )
        #============FRAMES==============
        self.frames = {}
        for F in (Main_window, Register_window,Login_window):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth = 1, relheight = 0.95, relx = 0, rely = 0.1)
        self.show_frame(Main_window)
    def show_frame(self, window):
        frame = self.frames[window]
        frame.tkraise()
    def crop_img(self, img, width, height):
        img_width, img_height = img.size
        return img.crop(((img_width - width) // 2, (img_height - height)//2, (img_width + width)//2, (img_height + height)//2))
    def circle_img(self, img,blur_radius, offset = 0):
        offset = blur_radius *2 + offset
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, img.size[0] - offset, img.size[1] + offset), fill = 255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
        result = img.copy()
        result.putalpha(mask)
        return result
    def clickonProfile(self, event):
        if Login_window.profile is None:
            self.show_frame(Login_window)
        else:
            profile_settings = Settings(self, Login_window.profile.user)
    def show_profile_pic(self, photo):
        self.body = Canvas(self.upper_frame, height = 60, width = 60, highlightthickness=0, bd =0, bg = 'black')
        self.body.place(x = 700, y = 5)
        self.img = Image.open(photo).resize((60,60), Image.ANTIALIAS)
        self.profile_img = self.crop_img(self.img, 0.8 * self.img.size[0], 0.8 * self.img.size[1])
        self.profile_img = self.circle_img(self.profile_img, 0.3)
        self.profile_img = ImageTk.PhotoImage(self.profile_img)
        self.cvs_profile = self.body.create_image(0,0, image = self.profile_img, anchor = NW)
        self.body.tag_bind(self.cvs_profile, '<ButtonPress - 1>', self.clickonProfile)

    def update_profile_pic(self,photo):
        self.body.place_forget()
        self.show_profile_pic(photo)

    def go_home(self, event):
       if Login_window.profile is not None:
            Login_window.profile.tkraise()

    @classmethod
    def show_profile(cls, frame):
        global name_upper_lablel
        name_upper_lablel = Label(frame, text = "             ")
        name_upper_lablel.place_forget()
        name_upper_lablel = Label(frame, text = cls.profile_name, bg = "black", fg = "white", anchor = NW)
        name_upper_lablel.place(x = 630, y = 25)

#@singleton
class Settings(Toplevel):
    def __init__(self,master, user):
        Toplevel.__init__(self)
        self.geometry("500x500")
        self.title("Settings")
        self.iconphoto(False,PhotoImage(file = logo_image_path))
        self.transient(master)
        self.user = user
        #======================BODY=================
        self.mainFrame = Frame(self, bg = "#4A4E54")
        self.mainFrame.pack(fill = 'both', expand = 1)
        self.create_body(App.profile_img)
        #===============LABELS====================
        self.nameLabel = Label(self.mainFrame, text = self.user.get_name(), bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        self.nameLabel.place(x = 80, y = 370)
        self.nameLabel2 = Label(self.mainFrame, text = "name: ", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        self.nameLabel2.place(x = 20, y  = 370)
        self.profileLabel = Label(self.mainFrame, text = "profile image", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        self.profileLabel.place(x = 200, y = 20)
        self.ErrorLabel = Label(self.mainFrame)
        #===================Buttons================
        self.change_name_button = Button(self.mainFrame, height = 2,width = 14, text = "change name", bg = "black", fg = "white", borderwidth = 0, command = self.change_name)
        self.change_name_button.place(x = 350, y = 70)
        self.change_password_button = Button(self.mainFrame, height = 2,width = 14, text = "change password", bg = "black", fg = "white", borderwidth = 0, command = self.change_password)
        self.change_password_button.place(x = 350, y = 130)
        self.change_picture_button = Button(self.mainFrame, height = 2,width = 14, text = "change picture", bg = "black", fg = "white", borderwidth = 0, command = self.change_picture)
        self.change_picture_button.place(x = 350, y = 190)
    def __del__(self):
        self.destroy()
    def create_body(self, photo):
        self.profile_img = ImageTk.PhotoImage(Image.open(photo).resize((300,300), Image.ANTIALIAS))
        self.body = Canvas(self.mainFrame, height = 300, width = 300, bg = "#4A4E54",highlightthickness=0, bd =0)
        self.body.place(x = 20, y = 50)
        self.img = self.body.create_image(0,0, image = self.profile_img, anchor = NW)
    def change_name(self):
        global nameLabel
        global applychanges_button
        self.nameLabel.place_forget()
        nameLabel = Entry(self.mainFrame, width = 17)
        nameLabel.place(x = 80, y = 370)
        applychanges_button = Button(self.mainFrame, height = 2,width = 14, text = "Apply changes", bg = "black", fg = "white", borderwidth = 0, command = self.update_name)
        applychanges_button.place(x = 350, y = 330)
        self.change_password_button.config(state = "disabled")
        self.change_picture_button.config(state = "disabled")

    def update_name(self):
        self.user.set_name(nameLabel.get())
        nameLabel.place_forget()
        new_name = self.user.get_name()
        self.nameLabel = Label(self.mainFrame, text = new_name, bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        self.nameLabel.place(x = 80, y = 370)
        self.change_password_button.config(state = "normal")
        self.change_picture_button.config(state = "normal")
        applychanges_button.destroy()
        Login_window.profile.post_profile_name(self.user.get_name())

    def change_password(self):
        global passwordold_e
        global passwordnew_e 
        global applychanges_button
        global passwordoldLabel
        global newpasswordLabel
        passwordoldLabel = Label(self.mainFrame, text = "Old pass", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        passwordoldLabel.place(x = 20, y = 400)
        newpasswordLabel = Label(self.mainFrame, text = "New pass", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
        newpasswordLabel.place(x = 20, y = 430)
        passwordold_e = Entry(self.mainFrame,show = "*", width = 17)
        passwordold_e.place(x = 110, y = 400)
        passwordnew_e = Entry(self.mainFrame,show = "*", width = 17)
        passwordnew_e.place(x = 110, y = 430)
        self.change_picture_button.config(state = "disabled")
        self.change_name_button.config(state = "disabled")
        applychanges_button = Button(self.mainFrame, height = 2,width = 14, text = "Apply changes", bg = "black", fg = "white", borderwidth = 0, command = self.update_password)
        applychanges_button.place(x = 350, y = 330)

    def update_password(self):
        self.ErrorLabel.place_forget()
        if (passwordold_e.get() == self.user.password):
            if len(passwordnew_e.get()) < 5:
                self.ErrorLabel = Label(self.mainFrame, text = "Password too short", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
                self.ErrorLabel.place(x = 230, y = 400)
            elif passwordnew_e.get() is None:
                self.ErrorLabel = Label(self.mainFrame, text = "Field is empty", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
                self.ErrorLabel.place(x = 230, y = 400)
            else:
                self.user.set_password(passwordnew_e.get())
                self.user.password = passwordnew_e.get()
                self.change_name_button.config(state = "normal")
                self.change_picture_button.config(state = "normal")
                passwordnew_e.destroy()
                passwordold_e.destroy()
                passwordoldLabel.destroy()
                newpasswordLabel.destroy()
                self.ErrorLabel = Label(self.mainFrame, text = "Password changed ", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
                self.ErrorLabel.place(x = 230, y = 400)
                applychanges_button.destroy()
                
        else:
            self.ErrorLabel = Label(self.mainFrame, text = "Wrong password", bg ="#4A4E54", fg = "white", anchor = NW, font = "Verdana 10 bold")
            self.ErrorLabel.place(x = 200, y = 400)
    def change_picture(self):
        filename = filedialog.askopenfilename(initialdir = "E:/" , title = "select image", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpg")))
        self.user.update_profile_pic(filename)
        App.profile_img = self.user.get_profile_pic()
        self.body.place_forget()
        self.create_body(App.profile_img)
        app_init.update_profile_pic(App.profile_img)

class Main_window(Frame):
    def __init__(self,controller):
        Frame.__init__(self)
        #============Images================
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.exit_button_image = ImageTk.PhotoImage(Image.open(Exit_image_path).resize((210,95), Image.ANTIALIAS))
        self.login_button_image = ImageTk.PhotoImage(Image.open(Login_image_path).resize((210,95), Image.ANTIALIAS))
        self.register_button_image = ImageTk.PhotoImage(Image.open(Register_image_path).resize((210,95), Image.ANTIALIAS))
        #============BACKGROUND================
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
        self.body.create_text(30,30, text = "This is a crypto gambling app. Register and have fun", fill = "white",anchor = NW)
        #============BUTTONS===============
        self.register_button = Button(self.body,height = 60, width = 170, image = self.register_button_image, borderwidth =0,command = lambda:controller.show_frame(Register_window))
        self.register_button.place(relx = 0.4, rely = 0.4)
        self.login_button = Button(self.body,height = 60, width = 170, image = self.login_button_image, borderwidth =0,bg ='grey', command = lambda:controller.show_frame(Login_window))
        self.login_button.place(relx = 0.4, rely = 0.55)
        self.exit_button = Button(self.body,height = 60, width = 170, image = self.exit_button_image, borderwidth =0,bg ='grey', command = self.quit)
        self.exit_button.place(relx = 0.4, rely = 0.7)
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)

class Register_window(Frame):
    def __init__(self,controller):
        Frame.__init__(self)
        #===========IMAGES==================
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.back_button_image = ImageTk.PhotoImage(Image.open(Back_image_path).resize((210,95), Image.ANTIALIAS))
        self.submit_button_image = ImageTk.PhotoImage(Image.open(Submit_image_path).resize((210,95), Image.ANTIALIAS))
        #============BACKGROUND===========
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
        #============BUTTONS==============
        self.submit_button = Button(self.body,height = 60, width = 170, image = self.submit_button_image, borderwidth =0,command = self.submit)
        self.submit_button.place(relx = 0.4, rely = 0.6)
        self.back_button = Button(self.body,height = 60, width = 170, image = self.back_button_image, borderwidth =0,command = lambda:[controller.show_frame(Main_window),self.delete_text(self.txtshow)])
        self.back_button.place(relx = 0.4, rely = 0.75)
        #==============ENTRYS============
        self.username_e = Entry(self.body, bg = "#4A4E54",width = 25, fg = 'white')
        self.username_e.place(relx = 0.45, rely = 0.3)
        self.password_e = Entry(self.body, bg = "#4A4E54",show = "*",width = 25, fg = 'white')
        self.password_e.place(relx = 0.45, rely = 0.37)
        self.passwordr_e = Entry(self.body, bg = "#4A4E54",show = "*",width = 25, fg = 'white')
        self.passwordr_e.place(relx = 0.45, rely = 0.44)
        self.name_e = Entry(self.body, bg = "#4A4E54",width = 25, fg = 'white')
        self.name_e.place(relx = 0.45, rely = 0.51)
        #==============LABELS=============
        self.body.create_text(280,180, text = "USERNAME", fill = 'white')
        self.body.create_text(280,220, text = "PASSWORD", fill = 'white')
        self.body.create_text(290,260,text ="RETYPE PASSWORD", fill = 'white')
        self.body.create_text(280,300,text ="NAME", fill = 'white')
        self.txtshow = self.body.create_text(280,120,text = "", fill = "white")
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)
    def submit(self):
        user = User(username = self.username_e.get(), password = self.password_e.get())
        if (not self.username_e.get()) or (not self.password_e.get()) or (not self.name_e.get()):
            messagebox.showinfo("Error","All entrys are mandatory")
        elif (" " in self.username_e.get()) or (" " in self.password_e.get()) or (" " in self.name_e.get()):
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
            del user
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
        elif user.search_username(self.username_e.get()) == False:
            messagebox.showinfo("Error","Username already taken")
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
        else:
            user.register(self.name_e.get(), profile_image)
            del user
            self.username_e.delete(0, END)
            self.password_e.delete(0, END)
            self.passwordr_e.delete(0, END)
            self.name_e.delete(0, END)
            self.txtshow = self.body.create_text(280,120,text = "you successfuly made an account", fill = "white")

    def delete_text(self,text):
            self.body.delete(text)

class Login_window(Frame):
    profile = None
    def __init__(self,controller):
        Frame.__init__(self)
        #===========IMAGES==================
        self.background_image = ImageTk.PhotoImage(Image.open(Login_bg_path))
        self.back_button_image = ImageTk.PhotoImage(Image.open(Back_image_path).resize((200,90), Image.ANTIALIAS))
        self.submit_button_image = ImageTk.PhotoImage(Image.open(Submit_image_path).resize((200,90), Image.ANTIALIAS))
        #============BACKGROUND===========
        self.body = Canvas(self, bg = 'white',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
        #============BUTTONS==============
        self.submit_button = Button(self.body,height = 60, width = 170,bg = 'white', image = self.submit_button_image, borderwidth =0, command = lambda:self.submit(controller))
        self.submit_button.place(relx = 0.4, rely = 0.6)
        self.back_button = Button(self.body,height = 60, width = 170, bg = 'white',image = self.back_button_image, borderwidth =0,command = lambda:controller.show_frame(Main_window))
        self.back_button.place(relx = 0.4, rely = 0.75)
        #==============LABELS=============
        self.body.create_text(280,180, text = "USERNAME")
        self.body.create_text(280,220, text = "PASSWORD")
        #==============ENTRYS============
        self.username_e = Entry(self.body, bg = "#4A4E54",width = 25, fg = 'white')
        self.username_e.place(relx = 0.45, rely = 0.3)
        self.password_e = Entry(self.body, bg = "#4A4E54",show = "*",width = 25, fg = 'white')
        self.password_e.place(relx = 0.45, rely = 0.37)
    def resize(self,event):
        img = Image.open(Login_bg_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)
    def submit(self, controller):
        global user
        user = User(username = self.username_e.get(), password = self.password_e.get())
        if user.login() == True:
            Login_window.profile = Profile_window(controller, user)
            Login_window.profile.place(relwidth = 1, relheight = 0.95, relx = 0, rely = 0.1)
            messagebox.showinfo("Login","welcome in")
            Login_window.profile.tkraise() 
            App.profile_img = user.get_profile_pic()
            app_init.update_profile_pic(App.profile_img)
        else:
            messagebox.showinfo("Error","Wrong username or password")
        
class Profile_window(Frame):
    def __init__(self, controller, user):
        Frame.__init__(self)
        self._username = user.username
        self.user = user
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.post_profile_name(self.user.get_name())
        App.profile_img = self._user.get_profile_pic()
        #============BACKGROUND===========
        self.body = Canvas(self, bg = 'white',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
         #==============LABELS=============
        self.money_text = self.body.create_text(20,20,text = "")
        self.update_money()
        #==============BUTTONS=============
        self.logout_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text = "LOGOUT", command = lambda:self.logout(self.user, controller) )
        self.logout_btn.place(x = 650, y = 450)
        self.balance_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text = "Balance", command = lambda:self.show_frame(Balance))
        self.balance_btn.place(x = 20, y = 80)
        self.Roulette_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="Roulette", command = lambda:[self.show_frame(Roulette),self.frames[Roulette].update_money()])
        self.Roulette_btn.place(x = 20, y = 160)
        self.Blackjack_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="BlackJack", command = lambda:self.show_frame(BlackJack))
        self.Blackjack_btn.place(x = 20, y = 240)
        self.Bet_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="Bet", command = lambda:self.show_frame(Bet))
        self.Bet_btn.place(x = 20, y = 320)
        #=================================
        self.frames = {}
        for F in (Roulette, Balance, BlackJack, Bet):
            frame = F(app_init,self, self.user)
            self.frames[F] = frame
            frame.place(relwidth = 1, relheight = 0.95, relx = 0, rely = 0.1)
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)
    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, us):
        self._user = us
    @user.deleter
    def user(self):
        del self._user

    def post_profile_name(self, name):
        App.profile_name = name
        App.show_profile(app_init.upper_frame)
    def logout(self, profile_user, controller):
        del profile_user
        Login_window.profile = None
        controller.show_frame(Main_window)
        controller.profile_img = profile_image
        controller.update_profile_pic(controller.profile_img)
        self.post_profile_name("            ")
    def show_frame(self, window):
        frame = self.frames[window]
        frame.tkraise()
    def update_money(self):
        self.body.delete(self.money_text)
        self.money = self._user.get_money()
        self.money_text = self.body.create_text(20,20, fill = "white", anchor = NW, font = "Verdana 12 bold", text = "Cash: {}$".format(self.money))

app_init = App()
app_init.mainloop()