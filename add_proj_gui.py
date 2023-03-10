from tkinter import *
from PIL import ImageTk, ImageTk
import sqlite3
from tkinter.filedialog import askopenfilename
from pathlib import Path
import os
from tkinter import messagebox


class add_project_gui:
    def __init__(self, MyGui):
        self.root = Toplevel()
        self.MyGui = MyGui
        ## keeps the add project window on top of the main window
        self.root.lift(aboveThis=self.MyGui.root)
        self.root.title('Add Project')
        self.root.geometry('650x240')

        # update background per theme
        self.root.config(bg=self.MyGui.settings.get_bg_color())

        ## Label for project name
        proj_name_lb = Label(self.root, text='Project Name', font=("Arial", 14),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())
        proj_name_lb.pack(pady=(20, 5))

        ## entry for project name
        self.proj_name_ent = Entry(self.root, width=35)
        self.proj_name_ent.pack(pady=(5,10))

        ## label for file location
        self.proj_location_lb = Label(self.root, text='Project Location', font=("Arial", 14),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())
        self.proj_location_lb.pack(pady=5)

        ## frame to hold the file entry and selector button 
        self.location_subframe = Frame(self.root, bg=self.MyGui.settings.get_bg_color())
        self.location_subframe.pack(padx=10, pady=5)

        ## entry for project file location
        self.proj_file_loc_ent = Entry(self.location_subframe, width=40)
        self.proj_file_loc_ent.pack(side=LEFT, padx=10)
        

        ##  function to open the file explorer selector 
        ## and get the file address
        def open_file_chooser():
            filename = askopenfilename(initialdir='~/Documents')
            self.proj_file_loc_ent.insert(END,filename)

        ## button for file selector
        self.file_selector_bt = Button(self.location_subframe, text='Select', 
            command = open_file_chooser)

        ## pack the file selector button
        self.file_selector_bt.pack(side=RIGHT)

        def close():
            self.root.destroy()
        
        ## function that collect name and file location and 
        ## stores the date in the db
        def collectAndStore():
            try:
                ## create a database
                conn = sqlite3.connect(os.path.expanduser(MyGui.settings.get_db_location()))

                ## create cursor
                c = conn.cursor()
                
                ## read the contents from  proj_name_ent
                temp_project_name = self.proj_name_ent.get()
                ## read the contents from proj_file_loc_ent
                temp_project_loc = self.proj_file_loc_ent.get()

                ## get the file name from the project location 
                temp_file_name = os.path.basename(temp_project_loc)
                
                ## need error correction, to make sure all info is provided 
                if(temp_project_name == ""):
                    messagebox.showerror(title="Error", message="Need project name")
                elif( temp_project_loc == ""):
                    messagebox.showerror(title="Error", message="Need project file location")
                else:
                    if(os.path.exists(temp_project_loc)):
                        # extract the actual file name from the file address
                        temp_file_name = os.path.basename(temp_project_loc)

                        ## convert the project file to binary
                        projectBinaryFiles = self.convertToBinaryData(temp_project_loc)

                        ### ---- small change, adding image as default 
                        ### TODO - change default image location from string to program settings attribute
                        projectImageBinary = self.convertToBinaryData("images/stan-medium.png")
                
                        ## write collected info into the database
                        c.execute(
                            '''INSERT INTO projects (proj_name, file_name, proj_files, proj_image) VALUES (?,?,?,?) ''',  
                            (temp_project_name, temp_file_name, projectBinaryFiles, projectImageBinary)
                        )
                
                        conn.commit()
                        ## alert the user that the project has been addede 
                        messagebox.showinfo(title="Project Status", message="Project added")
                        
                        # the project is created now, so close the window 
                        close();

                        ## redraw the results
                        MyGui.refresh()

                    else:
                        messagebox.showerror(title="Project Add Error", message="Valid file path required")

                c.close()
                
            except sqlite3.Error as error: 
                print("Failed to insert data into sqlite table", error)

        ## button to add / create project 
        self.proj_add_bt = Button(self.root, text="Add Project", command=collectAndStore)
        self.proj_add_bt.pack(padx=10, pady=5)

        self.root.mainloop()



    # Convert digital data to binary format
    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
