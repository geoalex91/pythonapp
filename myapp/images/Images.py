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

    def resize(self,image, height, width):
        r1 = image.size[0]/width
        r2 = image.size[1]/ height
        ratio = max(r1,r2)
        newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
        image = image.resize(newsize, Image.ANTIALIAS)
        return image

    def get_images(self):
        imgs = [self.exit,self.Login,self.back,self.submit, self.register]
        backgr = [self.background_1,self.background_2,self.background_3]
        img = []
        for i in imgs:
            i = ImageTk.PhotoImage(self.resize(Image.open(i), 70, 110))
            img.append(i)
        for i in backgr:
            i = ImageTk.PhotoImage(Image.open(i))
            img.append(i)
        return img
    


