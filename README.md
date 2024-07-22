# Automaten Code Generation for Codesys
With this scripts you can generate your own Module "frames". This is an example in how to work with Python-Scripts in CODESYS.
Following features are availabe:
### CreateEmptyFolderStructure
This script generates default folderstructure with the desirered "Modulename"

![image](https://github.com/user-attachments/assets/2583d1d8-e97f-4207-a71c-8aa0258a1e84)
![image](https://github.com/user-attachments/assets/420296fd-2f1a-453c-b5c4-f345daf584de)

### CreateEmptyPrg
This Script generates the folderstructure from above and in addition an PRG-Block with the modulname and options:

![image](https://github.com/user-attachments/assets/704703c1-3d39-400c-8d7d-0b75c63bc867)

You can choose following options:
1. Enable       -> The PRG-Block will have an enable input and internal enable handling
2. Init         -> The PRG-Block will have an init-routine, with mInit method
3. Performance  -> will ad an instance of fbTimeMeasurement to measure the perforamance of the PRG
   
![image](https://github.com/user-attachments/assets/3e09ccbb-e0b7-4b11-be21-387310db0e70)
![image](https://github.com/user-attachments/assets/4e9d18d9-d72a-4bcd-b661-2e435f8ff689)

### CreateModule
This script generates a "Module" or Functionblock, with diverse options and interfaces:
You can choose following options:
1. Ack     -> input for ackknowledgement handling
2. mode    -> for mode handling
3. ST_Config -> generates an configuration struct for the module
4. VISU_ITF  -> generates an Interface for Visualization or Scada
   
![image](https://github.com/user-attachments/assets/f8494d05-27b4-432c-bc42-05a6e6e83c19)
![image](https://github.com/user-attachments/assets/61facfaf-dcaa-47f9-a00d-72329c835dd0)
![image](https://github.com/user-attachments/assets/5612ce02-53ba-49ee-a248-57925c217e03)
