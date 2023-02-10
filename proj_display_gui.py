from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from functools import partial
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno


db_file='stl_manager.db'

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
#def open_file_chooser():
#    filename = askopenfilename()
#    self.proj_file_loc_ent.insert(END,filename)




class project_display_gui:

    def __init__(self, mainGui, prj_name):

        self.project_name = prj_name
        self.MyGui = mainGui

        ## explaination for Toplevel: https://stackoverflow.com/questions/20251161/tkinter-tclerror-image-pyimage3-doesnt-exist
        self.root = Toplevel()
        self.root.geometry('550x650')

        ## get the project id 
        self.project_id = self.get_project_id()

        # get the project image out of the database
        tempImageBinary = self.get_db_image(self.project_id)

        #convert the image back to digital and set as local image
        tempImage = PhotoImage(convertToDigitalData(tempImageBinary, "tempImage"))
        
        # in order to re-size the photoimage, we need to make it an Image first
        stl_img = Image.open("./tempImage")
        # now resize it 
        resized_stl_img = stl_img.resize((250, 350))
        ## now we have to use "ImageTk.PhotoImage, because the regular 
        ## PhotoImage only support png, and we want jpgs to work too
        self.photo_img = ImageTk.PhotoImage(resized_stl_img)

        ## making the lable into a button, so that the user can edit the 
        ## image of the project file 
        self.project_image_bt = Button(self.root, image=self.photo_img, 
                command=self.change_project_image)
        
        self.project_image_bt.pack(padx=10, pady=10)

        self.nameLb = Label(self.root, text="Project Name: " + prj_name, font=("None", 15))
        self.nameLb.pack(padx=10, pady=10)

        self.files_name = Label(self.root, text="File: " + self.get_file_name(prj_name), font=("None", 15))
        self.files_name.pack(padx=10, pady=10)

        #self.tagsLb = Label(self.root, text="Tags:")
        #self.tagsLb.pack(padx=10, pady=10)

        self.downloadBt = Button(self.root, text="Download Files", 
                command=partial(self.get_files, prj_name))
        self.downloadBt.pack(padx=10, pady=10)


        ## need a delete button
        #self.deleteBt = Button(self.root, text="Delete Project", fg='red', command=self.delete_entry)
        self.deleteBt = Button(self.root, text="Delete Project", fg='red', command=self.confirm_delete)
        self.deleteBt.pack(padx=10, pady=10)

        self.root.mainloop()


    # Convert digital data to binary format
    def convertToBinaryData(self,filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData


    def get_db_image(self,project_id):
        # open db
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())
        c = conn.cursor()

        # make statement 
        statement = ''' SELECT proj_image FROM projects 
                            WHERE proj_id = (?)
        '''
        # excecute
        c.execute(statement, (project_id,))
        output = c.fetchone()[0]

        # close db
        c.close()
        #print(output)
        return output

        # return image



    def set_db_image(self,image_location):
        # open db
        #conn = sqlite3.connect('stl_manager.db')
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())
        c = conn.cursor()

        ## first convert the file to a photoimage
        #test_img = PhotoImage(file="./images/stan-medium.png")
        #project_img = PhotoImage(image_location)

        # convert photoimage to binary
        try:
            image_blob = self.convertToBinaryData(image_location)
        except:
            pass
        

        # make statement 
        statement = 'UPDATE projects SET proj_image = (?) WHERE proj_id = (?)'
        c.execute(statement, (image_blob,self.project_id,))

        conn.commit()
        

        # close db
        c.close()


#    def open_file_chooser(self):
#        filename = askopenfilename(initialdir='~/Documents')
#        return filename

    def change_project_image(self):
        
        ## bring up a file explorer to let the user choose the new project image
         
        image_location = askopenfilename(initialdir='~/Documents')
        #print("image_location is: " + image_location)

        ## only set image if we receive a good image
        if((image_location == '') or (image_location == ())): ## add jpeg or png check
            pass  ## cancel was selected, nothing to do
        elif((image_location[-3:] == "jpeg") or (image_location[-3:] == "JPEG") or (image_location[-3:] == "png")
                or (image_location[-3:] == "PNG") or (image_location[-3:] == "jpg") or (image_location[-3:] == "JPG")): 
            try:
                self.set_db_image(image_location)
                self.MyGui.refresh()
                self.refresh()

            except:
                print("Error: Unable to change project image.")
        else: 
            messagebox.showerror(title="Change Image Error", message="Invalid file type selected")
            


    def get_project_id(self):
        # open the db
        #conn = sqlite3.connect('stl_manager.db')
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())
        c = conn.cursor()


        ## need to get the project id #
        ## get the project id # 
        statement = ''' SELECT proj_id FROM projects 
                            WHERE proj_name = (?)
        '''
        c.execute(statement, (self.project_name,))
        output = c.fetchone()[0]

        c.close()
        return output



    def confirm_delete(self):
        answer = askyesno(title='confirmation', message='Are you sure that you want to delete this project?')

        if answer: 
            self.delete_entry()


    def delete_entry(self):
        # open the db
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())
        c = conn.cursor()


        ## need to get the project id #
        ## get the project id # 
        statement = ''' SELECT proj_id FROM projects 
                            WHERE proj_name = (?)
        '''
        c.execute(statement, (self.project_name,))
        output = c.fetchone()[0]

        #print(output)

        # in a try
        try: 
            # do the remove 
            statement = 'DELETE FROM projects WHERE proj_id=? '
            c.execute(statement, (output,))
            conn.commit()
            #close the db
            c.close()

            # give the user confirmation
            messagebox.showinfo(title="Project Deleted", message="Project has been removed")

            # refresh the element display
            self.MyGui.refresh() ## need to import the main gui

            
            # destroy the frame 
            self.close()

        # else 
        except:
            # alert the user that it didnt work
            messagebox.showinfo(title="Error", message="Error, Project has not been removed")

        #close the db
        c.close()



    # function for getting (downloading) the files
    def get_files(self, prj_name):
    
        ## connect to the db
        #conn = sqlite3.connect('stl_manager.db')
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())

        ## make a cursor
        c = conn.cursor()

        ## make your query
        statement = ''' SELECT proj_files FROM projects WHERE proj_name = (?)'''
        c.execute(statement, (prj_name,))

        # save the output
        output = c.fetchone()[0]

        #print(output)
        ## for now, I need a filename 
        testFileName = self.get_file_name(prj_name)

        ## should put this in a try statement, and if worked, display a confirmation message 
        ## need to convert the files from binary
        try:
            ## get the location the user wants to place the download
            dlBaseLocation = filedialog.askdirectory(initialdir = "~/Downloads/")
            ## combine the download directory with the filename to make the full path name
            tempFullDlPath = dlBaseLocation + "/" + testFileName

            ## do the download
            convertToDigitalData(output, tempFullDlPath)
            ## show a message that says the it worked  
            messagebox.showinfo(title="Download Status", message="Download Successful")
        except:
            print("Sorry, download didn't work.")
            messagebox.showinfo(title="Download Status", message="Unable to download")

        ## open up a file explorer to let the user pick the location
        ## (provide the project name to the explorer)

        # close the db
        conn.close()


    def get_file_name(self, prj_name):
    
        ## connect to the db
        #conn = sqlite3.connect('stl_manager.db')
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.MyGui.settings.get_db_location())
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



    def refresh(self):
        self.root.destroy()
        self.__init__(self.MyGui, self.project_name)



    def close(self):
        self.root.destroy()

