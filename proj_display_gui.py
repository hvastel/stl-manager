from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from functools import partial
from tkinter import messagebox
from tkinter import filedialog



## needed functions (number = priority)
    # get_tags (4)
    # set_tags (3)
    # get_image (6)
    # set_image (5)
    # get_files (1)
    # set_files (7) 
    # set_project_name (8)
    # delete_entry (2)


# Convert binary to digital data format
def convertToDigitalData(blobData, filename):
    with open(filename, 'wb') as file:
        filename = file.write(blobData)
    return filename



##  function to open the file explorer selector 
## and get the file address
def open_file_chooser():
    filename = askopenfilename()
    self.proj_file_loc_ent.insert(END,filename)


# function for getting (downloading) the files
def get_files(prj_name):
    
    ## connect to the db
    conn = sqlite3.connect('stl_manager.db')

    ## make a cursor
    c = conn.cursor()

    ## make your query
    statement = ''' SELECT proj_files FROM projects WHERE proj_name = (?)'''
    c.execute(statement, (prj_name,))

    # save the output
    output = c.fetchone()[0]

    #print(output)
    ## for now, I need a filename 
    testFileName = get_file_name(prj_name)

    ## should put this in a try statement, and if worked, display a confirmation message 
    ## need to convert the files from binary
    try:
        ## get the location the user wants to place the download
        #dlBaseLocation = FileDialog.askopenfilename(initialdir = "~/Downloads/",
        #                                            title="select a location",
        #                                            fieltypes=("*.*"))

        convertToDigitalData(output, testFileName)
        ## show a message that says the it worked  
        messagebox.showinfo(title="Download Status", message="Download Successful")
    except:
        print("Sorry, download didn't work.")
        messagebox.showinfo(title="Download Status", message="Unable to download")



    ## open up a file explorer to let the user pick the location
    ## (provide the project name to the explorer)

    # close the db
    conn.close()


def get_file_name(prj_name):
    
    ## connect to the db
    conn = sqlite3.connect('stl_manager.db')
    ## make a cursor
    c = conn.cursor()

    # first get the file names
    statement = ''' SELECT file_name FROM projects WHERE proj_name = (?)'''
    c.execute(statement, (prj_name,))

    # save the output
    output = c.fetchone()[0]

    ## return the file name (the output)
    return output

    conn.close()


class project_display_gui:
    #global stl_img

    def __init__(self, prj_name):

        self.root = Tk()
        self.root.geometry('500x500')


        print("Project name is " + prj_name)
        ## in order to get the needed info, the project name is need. 
        ## will have to run some querys from the db to get the rest. 
                
        ## display the stl image
        #stl_img = PhotoImage(file="./images/stan-medium.png")
        #self.a_label = Label(self.root, image=stl_img, command=None)
        #self.a_label.image = stl_img  ## keep a reference :<
        #self.a_label.pack(padx=10, pady=10)

        self.nameLb = Label(self.root, text="Project Name: " + prj_name, font=("None", 15))
        self.nameLb.pack(padx=10, pady=10)

        self.files_name = Label(self.root, text="File: " + get_file_name(prj_name), font=("None", 15))
        self.files_name.pack(padx=10, pady=10)

        #self.tagsLb = Label(self.root, text="Tags:")
        #self.tagsLb.pack(padx=10, pady=10)

        self.downloadBt = Button(self.root, text="Download Files", 
                command=partial(get_files, prj_name))
        self.downloadBt.pack(padx=10, pady=10)


        ## need a delete button
        #self.deleteBt = Button(self.root, text="Delete Project", fg='red')
        #self.deleteBt.pack(padx=10, pady=10)

        ## make a frame to store the stl data

        ## label for stl name 
        ## lable for tags
        self.root.mainloop()

#project_display_gui()
