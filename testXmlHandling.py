from datetime import date
import re, time, os
import xml.dom.minidom as dom


f = open("test.xml", "r")

projectTree = dom.parseString(f.read())


print(projectTree.getElementsByTagName('fileHeader')[0].getAttribute('companyName'))
print(projectTree.getElementsByTagName('fileHeader')[0].getAttribute('productName'))
print(projectTree.getElementsByTagName('fileHeader')[0].getAttribute('productVersion'))

print(projectTree.getElementsByTagName('contentHeader')[0].getAttribute('name'))
print(projectTree.getElementsByTagName('contentHeader')[0].getAttribute('modificationDateTime'))
print(projectTree.getElementsByTagName('contentHeader')[0].getAttribute('organization'))
print(projectTree.getElementsByTagName('contentHeader')[0].getAttribute('author'))

