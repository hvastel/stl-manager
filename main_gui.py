from tkinter import *                                                                                                 
from tkinter import ttk 
import sqlite3
from PIL import ImageTk, Image
from add_proj_gui import *
from proj_display_gui import *
import math
from functools import partial
from os.path import exists

db_file='stl_manager.db'

def make_db():
    conn = sqlite3.connect(db_file)

    c = conn.cursor()

    c.execute("""CREATE TABLE projects(
        proj_id INTEGER PRIMARY KEY,
        proj_name TEXT,
        file_name TEXT,
        proj_files BLOB
        )""")

    conn.commit()
    conn.close()


#def show_display(project):
#    #project_display_gui(project)
#    project_display_gui(self, project)


## function to perform database a show all query in the database
def show_all_query(userRequest):
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
        #print("NOTE: went into the if...")
        #print(formattedUserRequest)

    conn = sqlite3.connect(db_file)

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
##----- end show_all_query()------

'''
## function to build out the results view (on the right side of 
## the program). This will build based on the search query 
## results, so it takes a cleaned up version of those. It
## also takes the mainViewFrame, so it can place the built 
## pieces into it. 
def viewResultsGenerator(projectList, elementFrame):

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
                

        ## button with image
        #button = Button(tempFrame, image=test_img, command=None)
        #buttonNameList[listPlace] = Button(tempFrame, image=test_img, command=show_display)
        buttonNameList[listPlace] = Button(tempFrame, image=test_img, 
                command=partial(self.show_display, project))
        buttonNameList[listPlace].image = test_img # keep a reference! (screw python...) 

        ## resizing image
        #photoimage = test_img.subsample(200, 200)

        #buttonNameList[listPlace] = ttk.Button(tempFrame, image = photoimage, command=isWorking)
        #buttonNameList[listPlace].image = photoimage
        
        #button.pack()
        buttonNameList[listPlace].pack()

        ## iterate the list position
        listPlace += 1;
            
        ## label
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

## --- end of viewResultsGenerator() ------
'''
            
            
class MyGUI:
    def __init__(self):
        ## need a check to see if the db is made.  if
        ## not, then make it. 
        if not(exists(db_file)):
            make_db()


        self.root = Tk()
        self.root.title('STL Manager')
        self.root.geometry('1250x700')

        ## function to open the "add new project" window
        def add_function():
            add_project_gui(self)
            #add_project_gui()


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
        #project_display_gui(project)
        project_display_gui(self, project)

    def getSearch(self):
        ## get the text from the search field 
        sometext = self.searchEntry.get()
        #print("the user search for:  " + sometext)
        return sometext

    def refresh(self):
        #self.refreshElements()
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
        self.canvas.pack(fill=BOTH, expand=1)

        ## get the contents of the search field 
        searchCritia = self.getSearch()

        ## will have to loop through a list to get the contents of the lables 
        self.viewResultsGenerator(show_all_query(searchCritia), self.elementFrame)
        #print("buildSubViewFrame send: " + searchCritia)
        #print(show_all_query(searchCritia))

        ## pack everything
        self.subViewFrame.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)
        self.sb.pack(side='right', fill="y", expand=0)





    ## function to build out the results view (on the right side of 
    ## the program). This will build based on the search query 
    ## results, so it takes a cleaned up version of those. It
    ## also takes the mainViewFrame, so it can place the built 
    ## pieces into it. 
    def viewResultsGenerator(self, projectList, elementFrame):

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
                
            ## button with image
            #button = Button(tempFrame, image=test_img, command=None)
            #buttonNameList[listPlace] = Button(tempFrame, image=test_img, command=show_display)
            buttonNameList[listPlace] = Button(tempFrame, image=test_img, 
                    command=partial(self.show_display, project))
            buttonNameList[listPlace].image = test_img # keep a reference! (screw python...) 

            ## resizing image
            #photoimage = test_img.subsample(200, 200)

            #buttonNameList[listPlace] = ttk.Button(tempFrame, image = photoimage, command=isWorking)
            #buttonNameList[listPlace].image = photoimage
        
            #button.pack()
            buttonNameList[listPlace].pack()

            ## iterate the list position
            listPlace += 1;
            
            ## label
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



## call the program
MyGUI()
