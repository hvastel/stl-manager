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
    db_location = '~/Documents/stl_manager.db'
    version = 0.12
    
    text_color = 'black'
    bg_Color = '#d9d9d9' # light gray
    comp_color = '#d9d9d9' # light gray

    def get_db_location(self):
        return self.db_location

    def set_db_location(self,given_locaiton):
        self.db_location = given_locaiton

    def get_version(self):
        return self.version

    def set_theme(self, theme_number):
        if (theme_number == 0): 
            # set default theme
            self.text_color = 'black'
            self.bg_Color = '#d9d9d9'
            self.comp_color = '#d9d9d9'

        elif (theme_number == 1):
            # set dark theme
            self.text_color = 'white'
            self.bg_Color = '#424242'
            self.comp_color = '#9e9e9e'
        else:
            # do nothing
            pass

    def get_text_color(self):
        return self.text_color

    def get_bg_color(self):
        return self.bg_Color

    def get_comp_color(self):
        return self.comp_color
        

            
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
        self.db_file = os.path.expanduser(self.settings.get_db_location())

        ## need a check to see if the db is made.  if
        ## not, then make it. 
        if not(exists(self.db_file)):
            self.make_db()


        self.root = Tk()
        self.root.title('STL Manager')
        self.root.geometry('1250x700')
        ## set Icon 
        self.root.iconphoto(True, PhotoImage(file='images/app-logo.png'))
        # update program main background per theme
        self.root.config(bg=self.settings.get_bg_color())
        

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
            filename = asksaveasfilename(initialdir='~/Documents')

            ## check if file exsist and verify correct type
            if (filename == ()): ## cancel was pressed
                pass
            elif (filename == ''): ## empty filename given
                pass
            else:
                ## append '.db' to the filename
                filename = filename + '.db'

                ## set the settings new location in the settings object
                self.settings.set_db_location(filename)
                db_file = self.settings.get_db_location()
            
                self.store_settings()

                ## make a new db at the new location 
                self.make_db()

                #refresh the display view
                self.refresh()

        def open_db():
            #filename = askopenfilename()
            filename = askopenfilename(initialdir='~/Documents')

            ## check if file exsist and verify correct type
            if ((filename == ()) or (filename == '')): ## cancel was pressed
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
            a_about = aAbout(self)

        def show_info():
            proj_info = project_info(self)

        def exit_program():
            self.root.destroy()

        def set_theme_default():
            # load dark colors preset
            self.settings.set_theme(0)
            # re-apply widget colors, (except in subviewframe)
            self.redraw_colors()
            # do a refresh to get all widgets in subviewframe
            self.refresh()
            #save the settings 
            self.store_settings()

        def set_theme_dark():
            # load dark colors preset
            self.settings.set_theme(1)
            # re-apply widget colors, (except in subviewframe)
            self.redraw_colors()
            # do a refresh to get all widgets in subviewframe
            self.refresh()
            #save the settings 
            self.store_settings()

        
        ## add the menu stuff 
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Database", command=new_db)
        self.filemenu.add_command(label="Open Database", command=open_db)
        self.filemenu.add_command(label="Quit", command=exit_program)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.viewmenu = Menu(self.menubar, tearoff=0)
        ## submenu
        self.theme_submenu = Menu(self.viewmenu, tearoff=0)
        self.theme_submenu.add_command(label='Default', command=set_theme_default)
        self.theme_submenu.add_command(label='Dark', command=set_theme_dark)
        self.viewmenu.add_cascade(label="Themes", menu=self.theme_submenu)
        
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Info", command=show_info)
        self.helpmenu.add_command(label="About", command=open_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)


        ## defining the area on the left of the program that will hold
        ## the search feature
        self.mainSearchFrame = Frame(self.root, bg=self.settings.get_bg_color())
        self.mainSearchFrame.pack(side=LEFT)

        ## defining a container to hold the search field and button
        self.searchFrame = Frame(self.mainSearchFrame, bg=self.settings.get_bg_color())
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
        self.mainViewFrame = LabelFrame(self.root, text='Results', bg=self.settings.get_bg_color())


        ## make the mainViewFrame match the theme
        self.mainViewFrame.configure(background=self.settings.get_bg_color())
        ## pack it
        self.mainViewFrame.pack(side=RIGHT, fill="both", expand=True, padx=25, pady=25)


        ## call a function that will handle the building of the subViewFrame.  
        self.buildSubViewFrame()

        self.root.mainloop()

    def show_display(self,project_id):
        project_display_gui(self, project_id)

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
        #self.subViewFrame = Frame(self.mainViewFrame, bg=self.settings.get_comp_color())
        self.subViewFrame = Frame(self.mainViewFrame)
        ## must pack subViewFrame later

        ## make a canvas (needed to support scrollable frame
        self.canvas = Canvas(self.subViewFrame, bg=self.settings.get_comp_color())

        ## making the scrollbar
        ### note: scrollable frame are a HUGE PAIN! 
        ## used this site for reference: https://blog.teclado.com/tkinter-scrollable-frames/
        self.sb = Scrollbar(self.subViewFrame, orient=VERTICAL, command=self.canvas.yview)
        self.sb.pack(side='right', fill="y", expand=0)

        ## make a frame that will only hold the results elements
        self.elementFrame = Frame(self.canvas, bg=self.settings.get_comp_color())
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
            tempFrame = Frame(elementFrame, bg=self.settings.get_comp_color())


            ###   --- set up the images here ---

            ## first get the project id
            temp_project_id = self.get_project_id(project)
            #print("got project id: " + str(temp_project_id))

            ## next, with the project id, get the image file
            temp_image_binary = self.get_db_image(temp_project_id) 
            
            ## send the binary to the prep_image fuction for conversion and resizing
            resized_stl_img = self.prep_image(temp_image_binary)

            ## button with image
            buttonNameList[listPlace] = Button(tempFrame, image=resized_stl_img, 
                    #command=partial(self.show_display, project))
                    command=partial(self.show_display, temp_project_id))
            
            buttonNameList[listPlace].image = resized_stl_img # keep a reference!  
        
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
                Label(tempFrame, text=sortenedProjectName, bg=self.settings.get_comp_color()).pack()
            else:
                # just pack the project label
                Label(tempFrame, text=project, bg=self.settings.get_comp_color()).pack()

        
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
        conn = sqlite3.connect(os.path.expanduser(self.settings.get_db_location()))

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
        conn = sqlite3.connect(os.path.expanduser(self.settings.get_db_location()))

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

        conn = sqlite3.connect(os.path.expanduser(self.settings.get_db_location()))

        c = conn.cursor()

        c.execute("""CREATE TABLE projects(
            proj_id INTEGER PRIMARY KEY,
            proj_name TEXT,
            file_name TEXT,
            proj_files BLOB,
            proj_image BLOB,
            proj_notes TEXT
            )""")

        conn.commit()
        conn.close()
        
    def redraw_colors(self):
        self.root.config(bg=self.settings.get_bg_color())
        self.mainSearchFrame.config(bg=self.settings.get_bg_color())
        self.searchFrame.config(bg=self.settings.get_bg_color())
        self.mainViewFrame.config(bg=self.settings.get_bg_color())


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

        conn = sqlite3.connect(os.path.expanduser(self.settings.get_db_location()))

        ## create cursor
        c = conn.cursor()

        ## show the db
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
