from tkinter import *                                                                                                 
from tkinter import ttk 
import sqlite3
from PIL import ImageTk, Image
from add_proj_gui import *
from proj_display_gui import *
from about_gui import aAbout
from info_gui import project_info
import math
from functools import partial
from os.path import exists
import pickle
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox


class program_settings:
    db_location = 'stl_manager.db'
    version = 0.05

    def get_db_location(self):
        return self.db_location

    def set_db_location(self,given_locaiton):
        self.db_location = given_locaiton
        

            
class MyGUI:
    def __init__(self):

        # make a settings object
        self.settings = program_settings()

        ## try to load the saved settings
        try: 
            self.load_settings()
            #print("after the load, the db location is: " + self.settings.get_db_location())
        except:
            pass

        # get the database location
        db_file = self.settings.get_db_location()
        #print("db_file location is: " +  db_file)

        ## need a check to see if the db is made.  if
        ## not, then make it. 
        if not(exists(db_file)):
            self.make_db()


        self.root = Tk()
        self.root.title('STL Manager')
        self.root.geometry('1250x700')
        

        ## function to open the "add new project" window
        def add_function():
            add_project_gui(self)


        ## a callback function, to help bind the searchEntry with the searchBt
        def enter_callback(event):
            self.refresh()

        def donothing():
            meh = 0

        def new_db():
            ## open a new messagedialogbox and get desired name / location 
            ## for the new db
            filename = asksaveasfilename()

            ## check if file exsist and verify correct type
            if (filename == ()): ## cancel was pressed
                pass
            else:
                ## append '.db' to the filename
                filename = filename + '.db'

                ## set the settings new location in the settings object
                self.settings.set_db_location(filename)
                db_file = self.settings.get_db_location()
            
                ## print out the location #### testing ######
                #print("DB file to be created: " + self.settings.get_db_location())

                self.store_settings()

                ## make a new db at the new location 
                self.make_db()

                #refresh the display view
                self.refresh()

        def open_db():
            filename = askopenfilename()

            ## check if file exsist and verify correct type
            if (filename == ()): ## cancel was pressed
                pass
            elif (filename[-3:] == '.db'):
                self.settings.set_db_location(filename)
                self.refresh()

                # update db settings 
                self.store_settings()
            else:
                # message that says the correct file type
                messagebox.showerror(title="Error", message="Invalid file type")


        def open_about():
            a_about = aAbout()

        def show_info():
            proj_info = project_info(self)


        
        ## add the menu stuff 
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Database", command=new_db)
        self.filemenu.add_command(label="Open Database", command=open_db)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Info", command=show_info)
        self.helpmenu.add_command(label="About", command=open_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)


        ## defining the area on the left of the program that will hold
        ## the search feature
        self.mainSearchFrame = Frame(self.root, highlightbackground="blue")
        self.mainSearchFrame.pack(side=LEFT)

        ## defining a container to hold the search field and button
        self.searchFrame = Frame(self.mainSearchFrame)
        self.searchFrame.pack()

        ## defining the search field and button
        self.searchEntry = Entry(self.searchFrame)
        self.searchBt = Button(self.searchFrame, text="search", command=self.refresh)

        ## allowing searches to be done by pressing the enter key
        self.searchEntry.bind('<Return>', enter_callback)

        ## packing the search field and button
        self.searchEntry.pack(side=LEFT, padx=10)
        self.searchBt.pack(side=RIGHT, pady=10)

        ## defining and packing the "New Project" button
        self.newProjectBt = Button(self.mainSearchFrame, text=" Add Project", command=add_function)
        self.newProjectBt.pack()

        #### ----- Now building the right side ---------
        
        ## defining the main right area of the program. This area
        ## will hold the search results, and will show all the
        ## STL projects in general.
        self.mainViewFrame = LabelFrame(self.root, text='Results')
        self.mainViewFrame.pack(side=RIGHT, fill="both", expand=True, padx=25, pady=25)

        ### note: scrollable frame are a HUGE PAIN! 
        ## used this site for reference: https://blog.teclado.com/tkinter-scrollable-frames/

        ## call a function that will handle the building of the subViewFrame.  
        self.buildSubViewFrame()

        self.root.mainloop()

    def show_display(self,project):
        project_display_gui(self, project)

    def getSearch(self):
        ## get the text from the search field 
        sometext = self.searchEntry.get()
        return sometext

    def refresh(self):
        self.subViewFrame.destroy()
        self.buildSubViewFrame()


    ## a function that will handle the building of the subViewFrame.  This is
    ## needed because these steps will have to be performed repeatedly for 
    ## refresh capability. 
    def buildSubViewFrame(self):

        ## while mainViewFrame holds the entire right side of the program, 
        ## subViewframe is a container that will keep the the results element frame 
        ## and the scrollbar together  
        self.subViewFrame = Frame(self.mainViewFrame)
        ## must pack subViewFrame later

        ## make a canvas (needed to support scrollable frame
        self.canvas = Canvas(self.subViewFrame)

        ## making the scrollbar
        ### note: scrollable frame are a HUGE PAIN! 
        ## used this site for reference: https://blog.teclado.com/tkinter-scrollable-frames/
        self.sb = Scrollbar(self.subViewFrame, orient=VERTICAL, command=self.canvas.yview)
        self.sb.pack(side='right', fill="y", expand=0)

        ## make a frame that will only hold the results elements
        self.elementFrame = Frame(self.canvas)
        ### DONT PACK THE ELEMENTFRAME!!! Its handled by the canvas window

        self.elementFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0,0), window=self.elementFrame, anchor='nw')

        # configure the canvas to make scrolling function
        self.canvas.configure(yscrollcommand=self.sb.set)

        ## get the contents of the search field 
        searchCritia = self.getSearch()

        ## will have to loop through a list to get the contents of the lables 
        self.viewResultsGenerator(self.show_all_query(searchCritia), self.elementFrame)

        ## pack everything
        self.subViewFrame.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)





    ## function to build out the results view (on the right side of 
    ## the program). This will build based on the search query 
    ## results, so it takes a cleaned up version of those. It
    ## also takes the mainViewFrame, so it can place the built 
    ## pieces into it. 
    def viewResultsGenerator(self, projectList, elementFrame):

        ## sorting the projectList so that the results will appear 
        ## in alphabetical order
        projectList.sort()
        

        test_img = PhotoImage(file="./images/stan-medium.png")
        ## make a list (array) to hold the frames that will be built
        frameList = []

    
        buttonNameList = []
        i = 0

        frameListSize = len(projectList)
        # need names for all the buttons
        while i < frameListSize:
            tempBtnName = "button_" + str(i)
            buttonNameList.append(tempBtnName)
            i += 1

        ## loop through the project list and make a frame for each
        ## with a botton and a label for each project
        listPlace = 0
        for project in projectList:
            tempFrame = Frame(elementFrame)


            ###   --- set up the images here ---

            ## first get the project id
            temp_project_id = self.get_project_id(project)
            #print("got project id: " + str(temp_project_id))

            ## next, with the project id, get the image file
            temp_image_binary = self.get_db_image(temp_project_id) 
            
            ## send the binary to the prep_image fuction for conversion and resizing
            resized_stl_img = self.prep_image(temp_image_binary)

            ## button with image
            #buttonNameList[listPlace] = Button(tempFrame, image=test_img, 
            buttonNameList[listPlace] = Button(tempFrame, image=resized_stl_img, 
                    command=partial(self.show_display, project))
            #buttonNameList[listPlace].image = test_img # keep a reference! (screw python...) 
            buttonNameList[listPlace].image = resized_stl_img # keep a reference! (screw python...) 

        
            #button.pack()
            buttonNameList[listPlace].pack()

            ## iterate the list position
            listPlace += 1;
            

            ## labels
            # if the length of the project is longer then 26 chars
            if(len(project) > 26):
                # make a variable to hold a shorten version of it
                # take the project name and cut it to 23 chars
                # append "..." at the end 
                sortenedProjectName = project[0:23] + '...'
                # pack the appended variable
                Label(tempFrame, text=sortenedProjectName).pack()
            else:
                # just pack the project label
                Label(tempFrame, text=project).pack()

        
            ## put the built frame in the list
            frameList.append(tempFrame)
            
        ## Now it time to set up the grid display. 
        ## get the size of the frameList
        listSize = len(frameList)
        listPos = 0
          
        ## arrange the frame elements in a grid in the viewframe, in 4 columns
        for y in range(math.ceil(listSize/4)):
            for x in range(4):
                try: 
                    frameList[listPos].grid(column=x, row=y, padx=5, pady=5)
                    ## for troubleshooting
                    #print("x is " + str(x) + "; y is " + str(y))
                    listPos += 1

                except:
                    #print("ran outta frames.")
                    pass

    def get_project_id(self, project_name):

        ## open the db
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.settings.get_db_location())

        ## create cursor
        c = conn.cursor()

        ## prep the query statement 
        statement = 'SELECT proj_id FROM projects WHERE proj_name = (?)'

        ## run the query
        c.execute(statement, (project_name,))
        output = c.fetchone()[0]
        
        # close the connector
        conn.close()

        return output
        


    def get_db_image(self, project_id):
        ## open the db
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.settings.get_db_location())

        ## create cursor
        c = conn.cursor()

        ## prep the query statement 
        statement = 'SELECT proj_image FROM projects WHERE proj_id = (?)'

        ## run the query
        c.execute(statement, (project_id,))
        output = c.fetchone()[0]
        
        # close the connector
        conn.close()

        return output



    def prep_image(self, aBinaryFile):
        convertToDigitalData(aBinaryFile, "tempImage")
        
        temp_image = Image.open("tempImage")
        resized_img = temp_image.resize((200, 300))
        resized_photo_img = ImageTk.PhotoImage(resized_img)
        # delete the tempImage file
        os.remove("tempImage")
        return resized_photo_img



    def make_db(self):
        #conn = sqlite3.connect(self.db_file)
        conn = sqlite3.connect(self.settings.get_db_location())

        c = conn.cursor()

        c.execute("""CREATE TABLE projects(
            proj_id INTEGER PRIMARY KEY,
            proj_name TEXT,
            file_name TEXT,
            proj_files BLOB,
            proj_image BLOB
            )""")

        conn.commit()
        conn.close()
        
        


    ## function to perform database a show all query in the database
    def show_all_query(self,userRequest):
        #print("Show_all_query recieved: " + userRequest)

        # declare the statement variable and set if for of there
        # is no search criteria
        statement = '''SELECT proj_name FROM projects'''

        intFlag = 0
        # if there is actually something to search, then prep the string and do the query
        if(userRequest != ""):
            intFlag += 1
            formattedUserRequest = "%" + userRequest + "%"
            statement = '''SELECT proj_name FROM projects WHERE proj_name LIKE ?''' 

        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(self.settings.get_db_location())

        ## create cursor
        c = conn.cursor()

        ## show the db
        #statement = '''SELECT proj_name FROM projects'''
        if (intFlag == 0):
            c.execute(statement)
        else:
            c.execute(statement , (formattedUserRequest,))


        # then take all records and put them in a list
        output = c.fetchall()

        # make a empty list to hold the cleaned up results from the query
        # in string form
        projectList = []

        # sadly, the elements in the query are surrounded by gargage.  Until 
        # a better way is found, I have to take several passes at the 
        # string, shaving away the un-needed chars. 
        for row in output:
            tempString = str(row)
            ## need to remove the first, 2nd to last, and last char
            tempString = tempString[:len(tempString)-1]
            tempString = tempString[:len(tempString)-1]
            tempString = tempString[1:]

            tempString = tempString[:len(tempString)-1]
            tempString = tempString[1:]

            ## once cleaned, we put the string in the projectList
            projectList.append(tempString)

        return(projectList)
    
        ### just test code to see the db working
        '''
        print("All the data")
        output = c.fetchall()
        for row in output:
            #print(row)
            print(*row, sep="\n")
        '''

        ## close the database
        conn.close()

    def load_settings(self):
        stl_mg_setting = open('stl_settings', 'rb')
        self.settings = pickle.load(stl_mg_setting)
        #print("Load_settings: value is: " + self.settings.get_db_location())
        stl_mg_setting.close()
        


    def store_settings(self):
        ## open the settings file
        ### change setting location to something that doesnt change
        stl_mg_setting = open('stl_settings', 'wb')

        ## convert settings object and write to file
        pickle.dump(self.settings, stl_mg_setting)
        #print("Store_settings: value is: " + self.settings.get_db_location())

        ## close the file
        stl_mg_setting.close()




## call the program
MyGUI()
