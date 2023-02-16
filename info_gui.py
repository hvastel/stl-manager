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
        self.bg_color = 'white'
        self.fg_color = 'black'


        self.db_name = self.get_db_name()
        self.db_location = self.get_db_location() 
        self.db_size = self.format_bytes(self.get_db_size())
        self.project_count = self.get_project_cnt()


        ## make main title label
        self.main_title_lb = Label(self.root, text='Current Database Information', font=('Arial', 20))
        self.main_title_lb.pack(padx=10, pady=10)


        ## make a frame to hold info
        self.info_frame = Frame(self.root, highlightbackground=self.fg_color, highlightthickness=2, bg=self.bg_color)
        self.info_frame.pack(padx=10, pady=(0,10))

        # will need at least 8 labels 
        self.db_name_lb = Label(self.info_frame, text='Database Name:', font=('Arial', 15), bg=self.bg_color,
                fg=self.fg_color)
        self.db_name_lb.grid(column=0, row=0, padx=(10,5), pady=5)
        self.db_location_lb = Label(self.info_frame, text='Database Locaiton:', font=('Arial', 15), bg=self.bg_color,
                fg=self.fg_color)
        self.db_location_lb.grid(column=0, row=1, padx=(10,5), pady=5)
        self.db_size_lb = Label(self.info_frame, text='Database Size:', font=('Arial', 15), bg=self.bg_color,
                fg=self.fg_color)
        self.db_size_lb.grid(column=0, row=2, padx=(10,5), pady=5)
        self.db_page_cnt_lb = Label(self.info_frame, text='Project Count:', font=('Arial', 15), bg=self.bg_color,
                fg=self.fg_color)
        self.db_page_cnt_lb.grid(column=0, row=3, padx=(10,5), pady=5)


        self.db_name_value_lb = Label(self.info_frame, text=self.db_name, bg=self.bg_color,
                fg=self.fg_color, font=('Arial',12)).grid(column=1, row=0, padx=15) 
        self.db_location_value_lb = Label(self.info_frame, text= self.db_location, bg=self.bg_color,
                fg=self.fg_color, font=('Arial', 12)).grid(column=1, row=1, padx=15)
        self.db_size_value_lb = Label(self.info_frame, text=self.db_size, bg=self.bg_color,
                fg=self.fg_color, font=('Arial', 13)).grid(column=1, row=2, padx=15)
        self.db_page_cnt_value_lb = Label(self.info_frame, text=self.project_count, bg=self.bg_color,
                fg=self.fg_color, font=('Arial', 13)).grid(column=1, row=3, padx=15)
        

        self.root.mainloop()



    def get_db_name(self):

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
        #file_size_Mb = file_size_in_bytes / 1000000
        #return math.floor(file_size_Mb)
        return file_size_in_bytes


    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'Kb', 2: 'Mb', 3: 'Gb', 4: 'Tb'}
        while size > power:
            size /= power
            n += 1
        size_string = str(math.floor(size)) + ' ' +  power_labels[n]
        return size_string

