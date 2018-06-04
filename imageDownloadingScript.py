#Program: imageDownloadingScript.py
#Programmer: Eric Davies
#Date: 27:5:2018
#Description: A script that checks if a task has been completed

import ee
import sys
import subprocess
import os.path
import json
import time

#############Function Block###################
def getNumberOfEERunningTasks():
	allEETasks = subprocess.Popen(["earthengine","task","list"],stdout=subprocess.PIPE).stdout.read().splitlines()
	incompleteEETasks = []
	for elementOfAllEETasks in allEETasks:
		if "COMPLETED" not in elementOfAllEETasks and "FAILED" not in elementOfAllEETasks and "CANCELLED" not in elementOfAllEETasks:
			incompleteEETasks.append(elementOfAllEETasks.split(" ")[2])
	return len(incompleteEETasks)

##############################################


fname = sys.argv[1]
#Get list of tasks
with open(fname) as f:
    content = f.readlines()
content = map(lambda s: s.strip(), content)
print(content[0])
#Get list of running tasks
runningTask = subprocess.Popen(["earthengine","task","list"],stdout=subprocess.PIPE).stdout.read().splitlines()
checkTasks = []
#print(runningTask)
for i in range(0,len(runningTask)):
	if "COMPLETED" not in runningTask[i]:
		checkTasks.append(runningTask[i].split(" ")[2])
#print(runningTask[0].split(" ")[4])
print(len(checkTasks))
print(getNumberOfEERunningTasks())
#Loop over list, remove any objects from tasklist that are running

allNoteDoneFiles = subprocess.Popen(["find","/Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete" + "/" + "users/alemlakes","-name","*.notDone.txt"], stdout=subprocess.PIPE).stdout.read()
allNoteDoneFiles = allNoteDoneFiles.replace(".notDone.txt","").replace("/Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete"+"/","")
allNoteDoneFilesList = allNoteDoneFiles.splitlines()

for x in allNoteDoneFilesList:
	print(x)
	 
