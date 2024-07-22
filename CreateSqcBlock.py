# encoding:utf-8
from __future__ import print_function
from datetime import date
import re
import os

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

INIT_SQC_METHOD="""\
// Initialize the Sequence
    THIS^.oMainSqc.stateInit(1);
"""

########################################################################### GENERATE ENUM
# generate enum with sequence steps
def generateSequenceEnum(moduleName, input_string):
    lines = input_string.strip().split('\n')
    contentString =  """\
{attribute 'qualified_only'}
{attribute 'strict'}
TYPE """ + moduleName+""" :
(
"""
        # Process each line
    for line in lines:
        # Split each line by space to separate the key and the comment
        parts = line.split(' ', 1)
        if len(parts) == 2:
            key, comment = parts
            key = key.upper()
            # Format the output line
            contentString = contentString + "\t"+key+", // "+comment+"\n"

    contentString = contentString +""");
END_TYPE"""

    return contentString


########################################################################### Write DECLARATION
# functions for code generation
def writeFbDeclaration(fwVersion, codesysVersion, actDate, fbName, ack, mode, optionConfig, optionVisu):
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
FUNCTION_BLOCK """
    contentString = contentString + str(fbName) + "\n"
    contentString = contentString + """VAR_INPUT
    //Name              Type            Init                                Comment
    xEnable             : bool;                                             // Enable Module""" 
    if ack == True: contentString = contentString + """
    xAck                : Bool;                                             // Acknowledge Error"""
    if mode == True: contentString = contentString + """
    xManual             : Bool;                                             // Manual Mode;"""
    if optionConfig != '': contentString = contentString + """
    utConfig            :""" + str(optionConfig) + ";                           // Module Configuration\n"
    contentString = contentString + """            
END_VAR
VAR_IN_OUT
    //Name              Type            Init                                Comment
    """
    if optionVisu != '': contentString = contentString + "utVisItf            :" + str(optionVisu) + ";\n"
    contentString = contentString + """
END_VAR
VAR_OUTPUT
    //  Name            Type            Init                                Comment
    wState              : word; //                                          // state of the functionblock
    uiSqcState          : uint;                                             // state of the Sequence
END_VAR
VAR 
    //Name              Type            Init                                Comment
    _xInit              : bool          := TRUE;                            // Init Cycle"""
    if ack == True: contentString = contentString + """
    _rtrigAck           : R_TRIG;                                           // Acknowledge Flag"""
    contentString = contentString + """
    _oMainSqc           : sqcHandler;                                       // Main Sequence Handler
END_VAR
VAR CONSTANT
    //  Name            Type            Init                                Comment
    
END_VAR
"""
    return contentString

########################################################################### WRITE IMPLEMENTATION
def writeFbSqcImplementation(ack, mode, enumName, input_string):
    lines = input_string.strip().split('\n')
    contentString = """\
    if NOT xEnable THEN RETURN; END_IF
//=========================================================
// +++ INIT +++
    mInit();
//=========================================================

//=========================================================
// +++ FLAGS & TIMER +++"""
    if ack == True: contentString = contentString + """
    _rtrigAck(CLK := xAck);"""
    contentString = contentString + """
//=========================================================

//=========================================================
// +++ INPUTS +++
	
//=========================================================

//=========================================================
// +++ PRIORITY KONDITIONS +++
	
//=========================================================

//=========================================================
// +++ SEQUENCE +++
    _oMainSqc();

    CASE _oMainSqc.uiActState OF
"""	
    # Process each line
    for line in lines:
        # Split each line by space to separate the key and the comment
        parts = line.split(' ', 1)
        if len(parts) == 2:
            key, comment = parts
            key = key.upper()
            # Format the output line
            contentString = contentString + "\t// +++ "+comment+" +++\n"
            contentString = contentString + "\t\t"+enumName+"."+key+":\n\t\t\t;\n"
            contentString = contentString + "\t\t\t"+"""IF False THEN _oMainSqc.nextState(PLACEHOLDER); END_IF

            """

    contentString = contentString + """
    ELSE
    ;
    END_CASE
//=========================================================

//=========================================================
// +++ OUTPUTS +++

//=========================================================

//=========================================================
// +++ VISU +++

//=========================================================

//=========================================================
// +++ ALARMS +++

//=========================================================
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


print("Generate default Module")
moduleName = system.ui.query_string("Module name")

########################################################################### FOLDER HANDLING
# create basic module structure
proj.create_folder(moduleName)
folder = proj.find(moduleName, recursive = True)[0]
folder.create_folder('DUT') 
folder.create_folder('POU') 
folder.create_folder('VIS')


# create options for module
print("Generate options for module")
res = system.ui.select_many("Please select one or more options", PromptChoice.OKCancel, PromptResult.OK, ("Ack", "Mode", "ST_Config", "VISU_ITF", "SQC in FB name"))
print("The returned result is: '%s'" % str(res)) # res is a tuple
if res[1][2]:   # choosen config option
    stConfig = createName('ST_CONF', moduleName)
    dut = folder.create_dut(stConfig)
    dut.textual_declaration.insert(2, 0, CONFIG_STRUCT)
else:
    stConfig = ''
if res[1][3]:   # choosen Visu option
    stVis = createName('ST_VIS', moduleName)
    dut = folder.create_dut(stVis)
    dut.textual_declaration.insert(2, 0, VISU_STRUCT)
else:
    stVis = ''
optionAck  = res[1][0]
optionMode = res[1][1]
optionSqc  = res[1][4]


########################################################################### ENUM AND SQC GENERATION
#read input 
print("Name your Steps + Comment")
res = system.ui.query_string("Name your Steps + Comment ", multi_line=True)
#create enum
enum = folder.create_dut(createName('ENUM_SQC', moduleName), DutType.Enumeration)
enum.textual_declaration.replace(generateSequenceEnum(createName('ENUM_SQC', moduleName), res))

# create module with chossen prefix
if optionSqc == True: namePrefix = 'FB_SQC' 
else: namePrefix = 'FB'
pou = folder.create_pou(createName(namePrefix, moduleName), PouType.FunctionBlock)
implementation = pou.textual_declaration.replace(writeFbDeclaration(FW_VERSION, CODESYS_VERSION, today,createName(namePrefix, moduleName), optionAck, optionMode, stConfig, stVis))

# create implementation in module
pou.textual_implementation.replace(writeFbSqcImplementation(optionAck, optionMode, createName('ENUM_SQC', moduleName), res))
# add init method to module
initMethod = pou.create_method('mInit', 'BOOL')
# write init method implementation
initMethod.textual_implementation.replace(INIT_METHOD)




print("DONE!")