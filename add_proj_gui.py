from tkinter import *
from PIL import ImageTk, ImageTk
import sqlite3
from tkinter.filedialog import askopenfilename
from pathlib import Path
import os
from tkinter import messagebox

db_file='stl_manager.db'

# Convert digital data to binary format
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


class add_project_gui:
    def __init__(self, MyGui):
        #self.root = Tk()
        self.root = Toplevel()
        self.root.title('Add Project')
        self.root.geometry('650x300')

        ## Label for project name
        proj_name_lb = Label(self.root, text='Project Name', font=("None", 14))
        proj_name_lb.pack(pady=20)

        ## entry for project name
        self.proj_name_ent = Entry(self.root, width=35)
        self.proj_name_ent.pack()

        ## label for file location
        self.proj_location_lb = Label(self.root, text='Project Location', font=("None", 14))
        self.proj_location_lb.pack(padx=10, pady=10)

        ## frame to hold the file entry and selector button 
        self.location_subframe = Frame(self.root)
        self.location_subframe.pack(padx=10, pady=10)

        ## entry for project file location
        self.proj_file_loc_ent = Entry(self.location_subframe, width=35)
        self.proj_file_loc_ent.pack(side=LEFT, padx=10)
        

        ##  function to open the file explorer selector 
        ## and get the file address
        def open_file_chooser():
            filename = askopenfilename()
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
                #conn = sqlite3.connect('stl_manager.db')
                conn = sqlite3.connect(db_file)

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
                        projectBinaryFiles = convertToBinaryData(temp_project_loc)

                        ### ---- small change, adding image as default 
                        #projectImageBinary = convertToBinaryData("/home/bernard/nfs/code/python3/stl-app/images/stan-medium.png")
                        projectImageBinary = convertToBinaryData("images/stan-medium.png")
                
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

                
                    ## troubleshooting
                    #statement = '''SELECT proj_id, proj_name  FROM projects'''
                    #showOutput = c.execute(statement)
                    #print(showOutput)
                    #for row in showOutput:
                    #    print(row)
                
                c.close()
                
            except sqlite3.Error as error: 
                print("Failed to insert data into sqlite table", error)

        ## button to add / create project 
        self.proj_add_bt = Button(self.root, text="Add Project", command=collectAndStore)
        self.proj_add_bt.pack(padx=10, pady=10)



        self.root.mainloop()
