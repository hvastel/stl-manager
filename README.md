# STL Manager README

## Purpose:

STL Manager is a program designed to help  with the task of organizing a large number of STL files.  Anyone who has been 3D printings for a length of time knows that keeping track of past print files can become a hassle, and finding an old STL file can be time consuming.  This program has been make with the intent to make the process of finding specific files faster and easier.  Also, even though the program is called 'STL Manager', it can be used to support all kinds of maker projects, with the ability to store any file type.  That means It can keep track of projects that incorporate CNC files, DXF, EPS, AI, CDR, PDFs, Word documents, or anything else that one needs. 

## How to run:

To program is written in python.  To run it just run:

```
python3 main_gui.py
```

## Usage guide:

The basic concept is simple.  the program keeps track of projects.  It has the ability to store only one file.  This can be a single STL or an archive file (such as a zip file) .  The Idea is that in most cases, you will be keeping your project in a zip file anyway.  To store your project files, all you need to do is to create a new project, give it a name, and select the file that you want.  Projects are stored in the database, and are displayed in the display window.  You can find project by either scrolling through the display window or by search.  Once you found your desired project you can download the files and you're all set.  