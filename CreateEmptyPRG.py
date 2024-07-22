# encoding:utf-8
from __future__ import print_function
from datetime import date
import re

today = date.today()

FW_VERSION      = 'FW27'
CODESYS_VERSION = 'V3.5 SP19 P2'

CONFIG_STRUCT="""\
    //Name              Type            Init                                Comment
    sName               : String(10);
"""

VISU_STRUCT="""\
    //Name              Type            Init                                Comment
    xCmdDummy           : BOOL;
    xStatDummy          : BOOL;
"""

INIT_METHOD="""\
// Initialize your module
IF THIS^._xInit Then
    ;
    THIS^._xInit := FALSE;
END_IF
"""
########################################################################### WRITE DECLARATION
# functions for code generation
def writePrgDeclaration(fwVersion, codesysVersion, actDate, prgName, enable, performance):
    contentString = """// ===================================
// MICHAEL DROST COPYRIGHT (2024)
// Firmware Version:    """
    contentString = contentString + str(fwVersion) + "\n"
    contentString = contentString + "// Codesys Verison:    "
    contentString = contentString + str(codesysVersion) + "\n"
    contentString = contentString + "// Release Date:       "
    contentString = contentString + str(actDate) + "\n"
    contentString = contentString + """// Author:           MDrost
// Functionality:
// ===================================
PROGRAM """
    contentString = contentString + str(prgName) + "\n"
    contentString = contentString + """VAR_INPUT
    //Name              Type            Init                                Comment""" 
    if enable == True: contentString = contentString + """
    xEnable             : bool;                                             // Enable Module"""
    contentString = contentString + """            
END_VAR
VAR 
    //Name              Type            Init                                Comment
    _xInit              : bool          := TRUE;                            // Init Cycle"""
    if performance == True: contentString = contentString + """
    oPerformance        : FbTimeMeasurementAdv;                             // Measure Performance of the PRG"""
    contentString = contentString + """
END_VAR
VAR CONSTANT
    //  Name            Type            Init                                Comment
END_VAR
"""
    return contentString

########################################################################### WRITE IMPLEMENTATION

def writePrgImplementation(enable, performance):
    if enable == True: contentString = """\
IF NOT xEnable THEN RETURN; END_IF """
    else: contentString = ''
    contentString = contentString + """
//=========================================================
// +++ INIT +++
    mInit();"""
    if performance == True: contentString = contentString + """
    oPerformance();"""
    contentString = contentString + """
//=========================================================

//=========================================================
// +++ FLAGS & TIMER +++
//=========================================================

//=========================================================
// +++ PROGRAMM +++
	
//=========================================================

//=========================================================
// +++ VISU +++

//=========================================================

//=========================================================
// +++ ALARMS +++

//========================================================="""
    if performance == True: contentString = contentString + """
    oPerformance.costs();"""
    contentString = contentString + """
"""
    return contentString

########################################################################### CREATE NAME

def createName(prefix, moduleName):
    # Regular expression to find all uppercase letters
    pattern = r'([A-Z])'
    # Substitute each uppercase letter with _ followed by the letter
    modified_string = re.sub(pattern, r'_\1', moduleName)
    result = str(prefix).upper() + modified_string.upper()
    return result




########################################################################### FUNCTION
proj = projects.primary


print("Generate PRG")
moduleName = system.ui.query_string("Module name")
proj.create_folder(moduleName)
folder = proj.find(moduleName, recursive = True)[0]



# create options for module
print("Generate options for module")
res = system.ui.select_many("Please select one or more options", PromptChoice.OKCancel, PromptResult.OK, ("Enable", "Init", "Performance"))
print("The returned result is: '%s'" % str(res)) # res is a tuple


# create module
pou = folder.create_pou(createName('PRG', moduleName), PouType.Program)
implementation = pou.textual_declaration.replace(writePrgDeclaration(FW_VERSION, CODESYS_VERSION, today,createName('PRG', moduleName), res[1][0], res[1][2]))
# create implementation in module
pou.textual_implementation.replace(writePrgImplementation(res[1][0], res[1][2]))
# add init method to module
initMethod = pou.create_method('mInit', 'BOOL')
# write init method implementation
initMethod.textual_implementation.replace(INIT_METHOD)


print("DONE!")
#
#
#print("Now we query a multi line string")
#res = system.ui.query_string("Please tell me a nice story about your life!", multi_line=True)
#if (res):
#    print("Huh, that has been a long text, at least %s characters!" % len(res))
#else:
#    print("Hey, don't be lazy!")
#
#print("Username and passwort prompts...")
#res = system.ui.query_password("Please enter your favourite password!", cancellable=True)
#if res:
#    print("Huh, it's very careless to tell me your favourite password '%s'!" % res)
#else:
#    print("Ok, if you don't want...")
#
#res = system.ui.query_credentials("Now, for real...")
#if res:
#    print("Username '%s' and password '%s'" % res) # res is a 2-tuple
#else:
#    print("Sigh...")