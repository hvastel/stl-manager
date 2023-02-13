from tkinter import *                                                                                                 
import sqlite3
import os
import math


class project_info:
    def __init__(self, mainGui):

        self.root = Toplevel()
        self.root.title("Info")
        self.root.geometry('600x250')
        self.mainGui = mainGui


        self.db_name = self.get_db_name()
        self.db_location = self.get_db_location() 
        self.db_size = self.get_db_size()
        self.project_count = self.get_project_cnt()

        self.db_name_label = Label(self.root, text="Database name: " + self.db_name, 
                font=('Arial',16))
        self.db_name_label.pack(padx=10, pady=(40,10))

        self.db_loc_label = Label(self.root, text="Database location: " + 
                self.db_location, font=('Arial', 14))
        self.db_loc_label.pack(padx=10, pady=10)

        self.db_size_label = Label(self.root, text="Database size:  " + str(self.db_size)
                + " Mb", font=('Arial', 14))
        self.db_size_label.pack(padx=10, pady=10)

        self.project_cnt_label = Label(self.root, text="Project count: " + str(self.project_count),
                font=('Arial', 14))
        self.project_cnt_label.pack(padx=10, pady=10)

        self.root.mainloop()



    def get_db_name(self):

        # read from settings
        tempLoc = self.mainGui.settings.get_db_location()
        the_db_name = os.path.basename(tempLoc)
        return the_db_name
        


    def get_db_location(self):

        tempLoc = self.mainGui.settings.get_db_location()
        the_db_location = os.path.dirname(tempLoc)
        return the_db_location


    def get_project_cnt(self):

        # open the db
        conn = sqlite3.connect(os.path.expanduser(self.mainGui.settings.get_db_location()))

        ## create cursor
        c = conn.cursor()

        # do a show all query and get a list 
        statement = '''SELECT proj_id FROM projects'''
        c.execute(statement)

        # then take all records and put them in a list
        output = c.fetchall()

        # close the db
        conn.close()

        # get the size of the list 
        proj_count = len(output)

        # return the number
        return proj_count


    def get_db_size(self):
        file_size_in_bytes = os.path.getsize(os.path.expanduser(self.mainGui.settings.get_db_location()))
        file_size_Mb = file_size_in_bytes / 1000000
        return math.floor(file_size_Mb)

