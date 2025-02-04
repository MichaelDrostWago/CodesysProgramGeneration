from __future__ import print_function
from datetime import date
import re
from scriptengine import *  # Import necessary modules

debug = False

today = date.today()

### Get Global Project Data ###
project_reference   = projects.primary                         
active_application  = project_reference.active_application      # Get the Active Application
application_name    = active_application.get_name()             # Get Application name
projectpath         = project_reference.path                    # Get Project Location
#project_name        = project_reference.name                    # Get Project Name    
#project_author      = project_reference.author   
#project_company     = project_reference.company 


def createDocument(filename, projectpath, project_name):
    """
    creates a file in the project directory
    
    Args:
        filename (str): The name to the file.
        projectpath (str): The Path of the Project.
        project_name (str): The name of the Project.
    """
    ## get Project Path
    delimiter           = projectpath.rfind("\\")                  # find delimiter in path, because absolute path prints also .project ending
    file_ending_size    = len(projectpath) - delimiter - 1
    absolutepath        = projectpath[0:len(projectpath) - file_ending_size]    # Get absolute path without .project ending
    filepath            = absolutepath + "\\" + filename+"_"+project_name+"_"+str(today)+".txt"   

    ## Open and Create File
    f = open(filepath,"w")
    f.write("")
    f.close()
    
    return filepath


def writeDocumentHeader(filepath, application_name, project_name, date):
    """
    Writes a header to the documentation file with the project name and current date.
    
    Args:
        filepath (str): the filepath + name.
        application_name (str): The name of the application.
        project_name (str): The name of the Project.
        date (str): The date.
    """
    f = open(filepath,"a")
    f.write("=" * 50 + "\n")
    f.write("Project Documentation\n")
    f.write("Date: "+str(date)+"\n")
    f.write("Project: " + project_name + "\n")
    f.write("Application: " + application_name + "\n")
    f.write("=" * 50 + "\n\n")
    f.close()


def print_object(treeobj, filepath):
  
    f = open(filepath,"a")

    # if the current object is a device, we print the name and device identification.
    if treeobj:
        
        #type = treeobj.type
        name = treeobj.get_name(True)
        if debug: print(name)
       # print(dir(treeobj.type)) ## print object definitions
        if treeobj.is_device:
            name = treeobj.get_name(True)
            deviceid = treeobj.get_device_identification()
            if debug: print("DEVICE: " + name + "  " + str(deviceid))
            f.write("DEVICE: " + name + "  " + str(deviceid)+ "\n")

        elif treeobj.is_folder:
            name = treeobj.get_name(True)
            if debug: print("FOLDER: " + name)
            f.write("FOLDER: " + name + "\n")

        elif str(treeobj.type) == "413e2a7d-adb1-4d2c-be29-6ae6e4fab820":
            name = treeobj.get_name(True)
            if debug: print("PRG: " + name)
            f.write("PRG: " + name+ "\n")
        elif str(treeobj.type) == "6f9dac99-8de1-4efc-8465-68ac443b7d08":
            name = treeobj.get_name(True)
            if debug: print("FB: " + name + "  "+ str(treeobj.type))
            f.write("FB: " + name + "\n")
        elif treeobj.is_task:
            name = treeobj.get_name(True)
            kind        = treeobj.kind_of_task
            priority    = treeobj.priority
            interval    = treeobj.interval
            if debug: print("TASK: " + name + "  " + str(kind)+ "  "+ str(priority)+ "  "+ str(interval))
            f.write("TASK: " + name + "  " + str(kind)+ "  "+ str(priority)+ "  "+ str(interval)+ "\n")
        elif treeobj.is_libman:
            for repo in librarymanager.repositories:
                if debug: print(repo)
                f.write(str(repo)+ "\n")
                for lib in librarymanager.get_all_libraries(repo):  
                    if debug: print(lib)
                    f.write(str(lib)+ "\n")
    
    f.close()




print("--- Creating Documentation Files ---")

filePath = createDocument("Docoumentation", projectpath, "Test")
writeDocumentHeader(filePath, application_name, "test", today)
print("--- at Path: "+filePath+" ---")


# We iterate over all top level objects and call the print_tree function for them.
for obj in project_reference.get_children():
    for child in obj.get_children(True):
        print_object(child, filePath)
   

print("--- Done! ---")