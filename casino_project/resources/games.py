from tkinter import *
from tkinter import ttk
from random import randint, uniform
from PIL import ImageTk, Image, ImageDraw, ImageFilter
import os
import time
from threading import Thread
abs_path = os.path.abspath(os.getcwd())
background_image_path = abs_path + r".\images\darkbitcoin.png"
roulette_path = abs_path + r".\images\roulette.png"

class Balance(Frame):
    def __init__(self, controller,profile, user):
        Frame.__init__(self)
        self.user = user
        self.profile = profile
        #================Body===============
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
        self.body.create_text(300,30, fill = "white", anchor = NW, font = "Verdana 12 bold", text = "Withdraw or deposit money")
        self.body.create_text(190,150, fill = "white", anchor = NW, font = "Verdana 10", text = "Amount of money")
        self.ErrorLabel = self.body.create_text(210,280)
        #===========Entry================
        self.money_e = Entry(self.body, width = 20)
        self.money_e.place(x = 320, y = 150)
        #=============LABELS===============
        self.money_text = self.body.create_text(20,20,text = "")
        self.update_money()
        #============BUTTONS=============
        self.withdraw_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="Withdraw", command = lambda:self.withdraw(self.money_e))
        self.withdraw_btn.place(x = 220, y = 200)
        self.deposit_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text = "Deposit", command = lambda:self.deposit(self.money_e))
        self.deposit_btn.place(x = 380, y = 200)
    
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)

    def withdraw(self,amount):
        self.body.delete(self.ErrorLabel)
        money = self.user.get_money()
        try:
            if money >= int(amount.get()):
                money -= int(amount.get())
                self.user.set_money(money)
                self.profile.update_money()
                self.update_money()
            else:
                self.ErrorLabel = self.body.create_text(210,280, fill = "white", anchor = NW, font = "Verdana 10", text = "You don't have enough money")
                amount.delete(0, END)
        except TypeError:
            self.ErrorLabel = self.body.create_text(210,280, fill = "white", anchor = NW, font = "Verdana 10", text = "Only numbers are accepted")
            amount.delete(0, END)

    def deposit(self, amount):
        self.body.delete(self.ErrorLabel)
        money = self.user.get_money()
        try:
            money += int(amount.get())
            self.user.set_money(money)
            self.profile.update_money()
            self.update_money()
        except TypeError:
            self.ErrorLabel = self.body.create_text(210,280, fill = "white", anchor = NW, font = "Verdana 10", text = "Only numbers are accepted")
            amount.delete(0, END)

    def update_money(self):
        self.body.delete(self.money_text)
        self.money = self.user.get_money()
        self.money_text = self.body.create_text(20,20, fill = "white", anchor = NW, font = "Verdana 12 bold", text = "Cash: {}$".format(self.money))
class Roulette(Frame):
    bets = ["odd", "even", "number", "range"]
    range_bet = {"0 - 5":tuple(range(6)), "6 - 10":tuple(range(6,11)), "11 - 15": tuple(range(11,16)), "16 - 20": tuple(range(16,21)), "21 - 25":tuple(range(21,26)),
        "26 - 30":tuple(range(26,31)),"31 - 36":tuple(range(31,37))}

    _values_angles = {tuple(range(10)):0, tuple(range(10,20)):32, tuple(range(20,30)):15,tuple(range(30,40)):19,tuple(range(40,50)):4,tuple(range(50,60)):21,tuple(range(60,70)):2,
        tuple(range(70,80)):25,tuple(range(80,90)):17,tuple(range(90,100)):34,tuple(range(100,110)):6,tuple(range(110,120)):27,tuple(range(120,130)):13,tuple(range(130,140)):36,
        tuple(range(140,150)):30,tuple(range(150,160)):8,tuple(range(160,170)):23,tuple(range(170,180)):10,tuple(range(180,190)):5,tuple(range(190,200)):24,tuple(range(200,210)):16,
        tuple(range(210,220)):33,tuple(range(220,230)):1,tuple(range(230,240)):20,tuple(range(240,250)):14,tuple(range(250,260)):31,tuple(range(260,270)):9,tuple(range(270,280)):22,
        tuple(range(280,290)):18,tuple(range(290,300)):29,tuple(range(300,310)):7,tuple(range(310,320)):28,tuple(range(320,330)):12,tuple(range(330,340)):35,tuple(range(340,350)):3,
        tuple(range(350,360)):26}
    money_bet = None
    def __init__(self, controller, profile, user):
        Frame.__init__(self)
        self.user = user
        self.controller = controller
        self.profile = profile
        #================IMAGES========================
        self.background_img = Image.open(background_image_path)
        self.roulette_img = Image.open(roulette_path).resize((300,300), Image.ANTIALIAS)
        self.roulette_image = ImageTk.PhotoImage(self.roulette_img)
        self.background_image = ImageTk.PhotoImage(self.background_img)
        #===============CANVAS===========================
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", lambda event:self.resize(event, self.background_img))
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
        self.canvas_img2 = self.body.create_image(250,50, image = self.roulette_image, anchor = NW)
        #==================LABELS=========================
        self.body.create_text(20,370, fill = "white", anchor = NW, font = "Verdana 10", text = "Amount of money")
        self.body.create_text(230,370, fill = "white", anchor = NW, font = "Verdana 10", text = "type of bet")
        self.number = self.body.create_text(520,340, fill = "white", anchor = NW, font = "Verdana 10 bold", text = "")
        self.body.create_line(380,20,400,50, arrow = LAST, fill = "red")
        self.ErrorLabel = self.body.create_text(30,330)
        self.money_text = self.body.create_text(20,20,text = "")
        self.update_money()
        #======================ENTRY=====================
        self.place_money_e = Entry(self.body, width = 10)
        self.place_money_e.place(x = 150, y = 370)
        self.bet_num_e = Entry(self.body, width = 10)
        self.box_range = ttk.Combobox(self.body, value = Roulette.bets)
        self.box = ttk.Combobox(self.body, value = Roulette.bets)
        self.box.current(0)
        self.box.bind("<<ComboboxSelected>>", self.selection)
        self.box.place(x = 330, y = 370)
        #=================BUTTONS====================
        self.placebet_button = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="Place money", command = self.place_money)
        self.placebet_button.place(x = 130, y = 410)
        self.spin_btn = Button(self.body, bg = "black", fg = "yellow",borderwidth = 0, height = 3, width = 12, font = "Verdana 10", text ="Spin", command = self.spin_button_thread)
        self.spin_btn.place(x = 350, y = 410)
    
    def resize(self,event, image):
        img = image.resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)

    def selection(self, event):
        self.bet_num_e.place_forget()
        self.body.delete(self.number)
        self.box_range.place_forget()
        if self.box.get() == "number":
            self.bet_num_e = Entry(self.body, width = 10)
            self.bet_num_e.place(x = 520, y = 370)
            self.number = self.body.create_text(520,340, fill = "white", anchor = NW, font = "Verdana 10 bold", text = "Number")
        elif self.box.get() == "range":
            self.number = self.body.create_text(520,340, fill = "white", anchor = NW, font = "Verdana 10 bold", text = "Select range")
            self.box_range = ttk.Combobox(self.body, value = list(Roulette.range_bet.keys()))
            self.box_range.current(0)
            self.box_range.place(x = 520, y = 370)

    def update_money(self):
        self.body.delete(self.money_text)
        self.money = self.user.get_money()
        self.profile.update_money()
        self.money_text = self.body.create_text(20,20, fill = "white", anchor = NW, font = "Verdana 12 bold", text = "Cash: {}$".format(self.money))

    def place_money(self):
        self.body.delete(self.ErrorLabel)
        try:
            if not self.place_money_e.get():
                self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "The entry is empty")
            elif " " in self.place_money_e.get():
                self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "The entry contains spaces")
                self.place_money_e.delete(0, END)
            elif int(self.place_money_e.get()) > self.user.get_money():
                self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "you don't have enough money")
                self.place_money_e.delete(0, END)
            else:
                self.money_bet = int(self.place_money_e.get())
        except ValueError:
            self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "Only numbers are accepted")
            self.place_money_e.delete(0, END)

    def spin_gen(self, img):
        angle = 5
        time_spin = round(uniform(5,12),2)
        while time_spin > 0:
            image = Image.open(img).resize((300,300), Image.ANTIALIAS).convert("RGBA")
            image = ImageTk.PhotoImage(image.rotate(angle))
            self.canvas_img2 = self.body.create_image(250,50, image = image, anchor = NW)
            yield (image, angle)
            self.controller.after_idle(self.spin_gen, img)
            if time_spin >5:
                time.sleep(0.01)
                angle +=5
                angle %= 360
                time_spin -= 0.01
            elif time_spin > 2:
                time.sleep(0.03)
                angle +=3
                angle %= 360
                time_spin -= 0.03
            else:
                time.sleep(0.05)
                angle +=2
                angle %= 360
                time_spin -= 0.05
                
    def spin(self):
        self.body.delete(self.ErrorLabel)
        if self.money_bet is None:
            self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You haven't bet any money!!")
        else:
            bet_type = self.box.get()
            money = self.user.get_money()
            if bet_type == "number":
                if not self.bet_num_e.get():
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "Write a number!!")
                    raise Exception("Write a number!!")
                elif type(int(self.bet_num_e.get())) == str:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "Only numbers are accepted!!")
                    raise ValueError("Only numbers are accepted!!")
                elif (int(self.bet_num_e.get()) > 36) or (int(self.bet_num_e.get()) < 0):
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "Numbers not in range!!")
                    raise Exception("Numbers not in range!!")
            for i ,j in self.spin_gen(roulette_path):
                self.roulette_image = i
                angle = j

            for key in self._values_angles.keys():
                if angle in key:
                    number = self._values_angles[key]
            if bet_type == "odd":
                if number%2 == 1:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You win!!")
                    money += self.money_bet
                    self.user.set_money(money)
                    self.update_money()
                else:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You lose!!")
                    money -= self.money_bet
                    self.user.set_money(money)
                    self.update_money()
            elif bet_type == "even":
                if number%2 == 0:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You win!!")
                    money += self.money_bet
                    self.user.set_money(money)
                    self.update_money()
                else:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You lose!!")
                    money -= self.money_bet
                    self.user.set_money(money)
                    self.update_money()
            elif bet_type == "number":
                if int(self.bet_num_e.get()) == number:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You win!!")
                    money += self.money_bet * 5
                    self.user.set_money(money)
                    self.update_money()
                else:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You lose!!")
                    money -= self.money_bet
                    self.user.set_money(money)
                    self.update_money()
            elif bet_type == "range":
                if number in self.range_bet[self.box_range.get()]:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You win!!")
                    money += self.money_bet * 2
                    self.user.set_money(money)
                    self.update_money()
                else:
                    self.ErrorLabel = self.body.create_text(30,330, fill = "red", anchor = NW ,text = "You lose!!")
                    money -= self.money_bet
                    self.user.set_money(money)
                    self.update_money()
            self.money_bet = None
            self.place_money_e.delete(0, END)

    def spin_button_thread(self):
        thread = Thread(target = self.spin)
        thread.start()

class BlackJack(Frame):
    def __init__(self, controller,profile, user):
        Frame.__init__(self)
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
    
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)

class Bet(Frame):
    def __init__(self, controller,profile, user):
        Frame.__init__(self)
        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.body = Canvas(self, bg = 'black',highlightthickness=0, bd =0)
        self.body.pack(fill = 'both', expand = 1)
        self.body.bind("<Configure>", self.resize)
        self.canvas_img = self.body.create_image(0,0, image = self.background_image, anchor = NW)
    
    def resize(self,event):
        img = Image.open(background_image_path).resize((event.width, event.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)
        self.body.itemconfig(self.canvas_img,image = self.background_image)