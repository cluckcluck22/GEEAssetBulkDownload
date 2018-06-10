#Program: CheckForDownloadProgress.py
#Programmer: Eric Davies
#Date: 8/6/2018
#Description: A script that checks for files that are on the EarthEngine but not on the local client

import sys
import subprocess
import os.path
import json
import time


######################Function Block##############################

def getListOfEERunningTasks():
    allFilesAndDirs = subprocess.Popen(["earthengine","ls","-r", repo], stdout=subprocess.PIPE)
    return allFilesAndDirs.stdout.read().splitlines()

####################Function Block End############################

repo = sys.argv[1]
syncRepository = sys.argv[2]

#Get List of EE Tasks
listOfAllEEObjects = getListOfEERunningTasks()

validImages = open("validImages.txt","w")
validFolders = open("validFolders.txt","w")
invalidFolders = open("invalidFolders.txt","w")
invalidImages = open("invalidImages.txt","w")

print(listOfAllEEObjects)

for x in listOfAllEEObjects:
	if(os.path.exists(syncRepository + x)):
		print("Exists " + x)
		itemInfo = subprocess.Popen(["earthengine","asset","info",x],stdout=subprocess.PIPE).stdout.read()
		itemJson = json.loads(itemInfo)
		if (itemJson['type'] == 'Folder'):
			print("Item is a folder that exists")
			validFolders.write(x+"\n")
		else:
			print("Item is a file, check if it contains")
			fileContents = subprocess.Popen(["ls", syncRepository + x], stdout=subprocess.PIPE).stdout.read()
			if len(fileContents) > 0:
				print("Valid image Location")
				validImages.write(x+"\n")
			else:
				print("Invalid image output folder")
				invalidImages.write(x+"\n")
	else:
		itemInfo = subprocess.Popen(["earthengine","asset","info",x],stdout=subprocess.PIPE).stdout.read()
		itemJson = json.loads(itemInfo)
		if (itemJson['type'] == 'Folder'):
			invalidFolders.write(x+"\n")
		else:
			invalidImages.write(x+"\n")

print("All Files checked")
			
validImages.close()
validFolders.close()
invalidFolders.close()
invalidImages.close()

print("End of Script")