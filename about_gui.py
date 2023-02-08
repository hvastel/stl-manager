from tkinter import *                                                                                                 


class aAbout:
    def __init__(self):

        self.root = Tk()

        self.title = "STL Manager"
        self.versionNumber = "0.05"
        self.creator = "Bernard Ugwu"

        self.root.geometry('300x200')
        self.root.title("Stl Manager About")

        self.titleLabel = Label(self.root, text=self.title, font=('Arial', 22))
        self.titleLabel.pack(padx=10, pady=(25,10))

        self.versionLabel = Label(self.root, text="Version: " + self.versionNumber, 
                font=('Arial', 15))
        self.versionLabel.pack( padx=10, pady=10)

        self.creatorLabel = Label(self.root, text="Creator:  " + self.creator, 
                font=('Arial', 15))
        self.creatorLabel.pack(padx=10, pady=10)

        self.root.mainloop()
