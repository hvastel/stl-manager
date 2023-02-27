from tkinter import *                                                                                                  
from PIL import ImageTk, Image


class aAbout:
    def __init__(self, MyGui):

        self.MyGui = MyGui

        #self.root = Tk()
        self.root = Toplevel()

        self.title = "STL Manager"
        self.versionNumber = str(self.MyGui.settings.get_version())
        self.creator = "Bernard Ugwu"

        self.root.geometry('500x450')
        self.root.title("Stl Manager About")

        # add a label to be the program icon
        self.icon_image = PhotoImage(file='images/app-logo.png') 
        self.icon_image_sub = self.icon_image.subsample(6,6)
        self.icon_lb = Label(self.root, image=self.icon_image_sub)
        self.icon_lb.image = self.icon_image_sub
        self.icon_lb.pack()


        self.titleLabel = Label(self.root, text=self.title, font=('Arial', 22))
        self.titleLabel.pack(padx=10, pady=(25,10))

        self.versionLabel = Label(self.root, text="Version: " + self.versionNumber, 
                font=('Arial', 15))
        self.versionLabel.pack( padx=10, pady=10)

        self.creatorLabel = Label(self.root, text="Creator:  " + self.creator, 
                font=('Arial', 15))
        self.creatorLabel.pack(padx=10, pady=10)

        self.root.mainloop()
