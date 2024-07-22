# encoding:utf-8
from __future__ import print_function

proj = projects.primary


print("Generate default structure")
res = system.ui.query_string("Modulename")

proj.create_folder(res)
folder = proj.find(res, recursive = True)[0]
folder.create_folder('DUT') 
folder.create_folder('POU') 
folder.create_folder('VIS')

print("DONE!")
