from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from functools import partial
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import tkinter.simpledialog
import os
import Pmw

db_file='stl_manager.db'


# Convert binary to digital data format
def convertToDigitalData(blobData, filename):
    with open(filename, 'wb') as file:
        filename = file.write(blobData)
    return filename



class project_display_gui:

    def __init__(self, mainGui, prj_id):

        self.MyGui = mainGui
        #self.project_name = prj_name
        self.project_id = prj_id
        self.project_name = self.get_project_name(prj_id)

        ## explaination for Toplevel: https://stackoverflow.com/questions/20251161/tkinter-tclerror-image-pyimage3-doesnt-exist
        self.root = Toplevel()
        self.root.geometry('950x950')


        ## add two frames for the left and right sides 
        self.left_frame = Frame(self.root)
        self.right_frame = Frame(self.root)
        self.left_frame.config(bg=self.MyGui.settings.get_bg_color())
        self.right_frame.config(bg=self.MyGui.settings.get_bg_color())

        self.left_frame.pack(side=LEFT, fill=Y, padx=(50,5), pady=50)
        self.right_frame.pack(side=RIGHT, fill=Y, padx=(5,50), pady=50)


        ## create a tooltip for help message on image button
        Pmw.initialise(self.root) #initializing it in the root window
        self.tip=Pmw.Balloon(self.root)


        self.text_color = 'white'

        self.bg_Color = '#424242'
        self.comp_color = '#9e9e9e'
        
        #self.root.config(bg = self.bg_Color)
        self.root.config(bg = self.MyGui.settings.get_bg_color())

        # get the project image out of the database
        tempImageBinary = self.get_db_image(self.project_id)

        #convert the image back to digital and set as local image
        tempImage = PhotoImage(convertToDigitalData(tempImageBinary, "tempImage"))
        
        # in order to re-size the photoimage, we need to make it an Image first
        stl_img = Image.open("./tempImage")
        # now resize it 
        #resized_stl_img = stl_img.resize((250, 350))
        resized_stl_img = stl_img.resize((350, 450))
        ## now we have to use "ImageTk.PhotoImage, because the regular 
        ## PhotoImage only support png, and we want jpgs to work too
        self.photo_img = ImageTk.PhotoImage(resized_stl_img)

        ## making the lable into a button, so that the user can edit the 
        ## image of the project file 
        self.project_image_bt = Button(self.left_frame, image=self.photo_img,  
                command=self.change_project_image)

        self.tip.bind(self.project_image_bt, "Click to change project image")
        
        self.project_image_bt.pack(padx=10, pady=(10,5))



        # button subframe for download and delete buttons
        self.bt_subframe = Frame(self.left_frame, bg=self.MyGui.settings.get_bg_color())
        self.bt_subframe.pack(side=BOTTOM)

        self.project_name_display_lb = Label(self.right_frame, text='Project Name:', font=('Arial', 18),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())

        self.project_name_display_lb.pack(pady=(75,5))
        
        self.project_name_lb = Label(self.right_frame, text=self.project_name, font=('Arial', 15),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())
        
        self.project_name_lb.pack(pady=(5,15))


        ## added edit button to change project name 
        self.editBt = Button(self.right_frame, text='Edit', bg=self.comp_color, command=self.edit_mode)
        self.editBt.pack()


        self.file_name_lb = Label(self.right_frame, text='File Name:', font=('Arial', 18),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())
        
        self.file_name_lb.pack(pady=(40,5))

        self.file_name = Label(self.right_frame, text=self.get_file_name(self.project_name), font=('Arial', 15),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())

        self.file_name.pack(pady=(5,15))


        self.notes_lb = Label(self.right_frame, text='Notes', font=('Arial', 15),
                fg=self.MyGui.settings.get_text_color(), bg=self.MyGui.settings.get_bg_color())
        self.notes_lb.pack(pady=(110,5))

        ## need a text widget for the notes
        self.notes_textwidget = Text(self.right_frame, width=30, height=10, font=('Arial',14), wrap=WORD)
        self.notes_textwidget.pack()

        ## load the notes from the db
        try:
            self.get_notes()
        except:
            pass

        # button to update notes
        self.notes_bt = Button(self.right_frame, text='Update', command=self.set_notes)
        self.notes_bt.pack(pady=5)


        #self.downloadBt = Button(self.root, text="Download Files", bg=self.comp_color, 
        #        command=partial(self.get_files, self.project_name))
        self.downloadBt = Button(self.bt_subframe, text="Download Files", bg=self.comp_color, 
                command=partial(self.get_files, self.project_name))

        self.downloadBt.pack(padx=10, pady=10)


        ## need a delete button
        #self.deleteBt = Button(self.root, text="Delete Project", fg='red', bg=self.comp_color, command=self.confirm_delete)
        #self.deleteBt.pack(padx=10, pady=10)
        self.deleteBt = Button(self.bt_subframe, text="Delete Project", fg='red', bg=self.comp_color, command=self.confirm_delete)
        self.deleteBt.pack(padx=10, pady=(10,100))

        self.root.mainloop()


    # Convert digital data to binary format
    def convertToBinaryData(self,filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData


    def get_db_image(self,project_id):
        # open db
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
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

        # return image
        return output




    def set_db_image(self,image_location):
        # open db
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
        c = conn.cursor()

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



    def change_project_image(self):
        
        ## bring up a file explorer to let the user choose the new project image
        image_location = askopenfilename(initialdir='~/Pictures')

        ## only set image if we receive a good image
        if((image_location == '') or (image_location == ())): ## add jpeg or png check
            pass  ## cancel was selected, nothing to do
        elif((image_location[-4:] == "jpeg") or (image_location[-4:] == "JPEG") or (image_location[-3:] == "png")
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
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
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
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
        c = conn.cursor()


        ## need to get the project id #
        ## get the project id # 
        statement = ''' SELECT proj_id FROM projects 
                            WHERE proj_name = (?)
        '''
        c.execute(statement, (self.project_name,))
        output = c.fetchone()[0]

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
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))

        ## make a cursor
        c = conn.cursor()

        ## make your query
        statement = ''' SELECT proj_files FROM projects WHERE proj_name = (?)'''
        c.execute(statement, (prj_name,))

        # save the output
        output = c.fetchone()[0]

        ## for now, we need the filename 
        testFileName = self.get_file_name(prj_name)

        ## try statement, and if worked, display a confirmation message 
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

        # close the db
        conn.close()


    def get_file_name(self, prj_name):
    
        ## connect to the db
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
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


    def get_project_name(self, project_id):

        ## connect to the db
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
        ## make a cursor
        c = conn.cursor()

        # first get the file names
        statement = ''' SELECT proj_name FROM projects WHERE proj_id = (?)'''
        c.execute(statement, (project_id,))
        
        # save the output
        output = c.fetchone()[0]

        ## return the file name (the output)
        return output
    
        conn.close()


    def refresh(self):
        self.root.destroy()
        self.__init__(self.MyGui, self.project_id)


    def close(self):
        self.root.destroy()


    def edit_mode(self):
        ## pull up a small dialog box asking for a new project name
        new_prod_name = tkinter.simpledialog.askstring(title='New project name', prompt="Please enter new project name")
        # if cancel is not selected, change the project name
        if(new_prod_name != None):
            self.set_project_name(new_prod_name)


    def set_project_name(self, new_prod_name):

        ## if the new project string is not null or empty
        if ((new_prod_name != None) or (new_prod_name != '')):

            # setup your sql command
            statement = 'UPDATE projects SET proj_name = (?) WHERE proj_id = (?)'
            
            # open the database 
            conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
            c = conn.cursor()

            # execute the command
            try:
                c.execute(statement, (new_prod_name,self.project_id,))
                conn.commit()
                self.refresh()
                #self.MyGui.refresh()
            except: 
                print("Error: attempted to update project name, db error")
                messagebox.showerror(title="Update Status", message="Unable to update project name")

            # close the db
            conn.close()


    def set_notes(self):

        ## get the contents of the notes text widget 
        note_text = self.notes_textwidget.get("1.0", "end-1c") 

        ## write them to the db
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
        c = conn.cursor()

        statement = 'UPDATE projects SET proj_notes = (?) where proj_id = (?)'

        try: 
            c.execute(statement, (note_text,self.project_id,))
            conn.commit()
        except:
            print("Error: attempted to update project notes, db error")
            messagebox.showerror(title="Update Status", message="Unable to update project notes")

        conn.close()


        


    def get_notes(self):

        #note_text = 'This is just some test text '

        # get the db record for the notes
        conn = sqlite3.connect(os.path.expanduser(self.MyGui.settings.get_db_location()))
        c = conn.cursor()

        statement = 'SELECT proj_notes FROM projects WHERE proj_id = (?)'

        try: 
            c.execute(statement, (self.project_id,))
            conn.commit()
        except:
            #print("Error: Unable to get notes text from database")
            pass

        output = c.fetchone()[0]
        conn.close


        ## place it in the notes text widget
        if (output != None):
            self.notes_textwidget.insert(END, output)
        #print(output)
