from tkinter import *
from PIL import ImageTk, ImageTk
import sqlite3
from tkinter.filedialog import askopenfilename
from new_main import *


# Convert digital data to binary format
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


#def refresh_main(MyGui):
#    MyGui.refresh_root()


class add_project_gui:
    #def __init__(self, MyGui):
    def __init__(self):
        self.root = Tk()
        self.root.title('Add Project')
        self.root.geometry('650x300')

        ## Label for project name
        proj_name_lb = Label(self.root, text='Project Name')
        proj_name_lb.pack(pady=20)

        ## entry for project name
        self.proj_name_ent = Entry(self.root, width=35)
        self.proj_name_ent.pack()

        ## label for file location
        self.proj_location_lb = Label(self.root, text='Project Location')
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
        
        ## function that collect name and file location and 
        ## stores the date in the db
        def collectAndStore():
            try:
                ## create a database
                conn = sqlite3.connect('stl_manager.db')

                ## create cursor
                c = conn.cursor()
                
                ## read the contents from  proj_name_ent
                temp_project_name = self.proj_name_ent.get()
                ## read the contents from proj_file_loc_ent
                temp_project_loc = self.proj_file_loc_ent.get()
                
                ## convert the project file to binary
                projectBinaryFiles = convertToBinaryData(temp_project_loc)
                
                ## write both into the database
                c.execute(
                    '''INSERT INTO projects (proj_name, proj_files) VALUES (?, ?) ''',  
                    (temp_project_name, projectBinaryFiles)
                )
                
                conn.commit()
                
                ## show the db
                statement = '''SELECT * FROM projects'''
                c.execute(statement)
                
                c.close()
                ## redraw the results
                #refresh_main(MyGui)
                
            except sqlite3.Error as error: 
                print("Failed to insert data into sqlite table", error)

        ## button to add / create project 
        self.proj_add_bt = Button(self.root, text="Add Project", command=collectAndStore)
        self.proj_add_bt.pack(padx=10, pady=10)



        self.root.mainloop()
