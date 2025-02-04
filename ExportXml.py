from __future__ import print_function
from datetime import date
import re, time, os
import xml.dom.minidom as dom
from scriptengine import *  # Import necessary modules

debug = False

today = date.today()

proj=projects.primary
origProjectFile=proj.export_xml(proj.get_children(True), recursive=True, export_folder_structure=True, declarations_as_plaintext=False)
newProjectFile=origProjectFile[1:len(origProjectFile)]


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




print("--- Creating Documentation Files ---")

filePath = createDocument("Docoumentation", projectpath, "Test")
print("--- at Path: "+filePath+" ---")


f = open(filePath, "w")
f.write(newProjectFile)
f.close()





print("--- Done! ---")