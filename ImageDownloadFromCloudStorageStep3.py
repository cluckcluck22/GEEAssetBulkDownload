#Program: ImageDownloadFromCoudStorage.py
#Programmer: Eric Davies
#Date: 28/5/2018
#Description: A script that downloads images from a cloud storage and downloads them to a local storage. Works only after the
#	AssetMirrorScript.py has been run as it relies on the images being saved to a cloud storage in order to run.

import sys
import subprocess
import ee
import os
import json
import time


TimeToSleepBetweenRuns = 60

CloudStorageBucketName = "gs://bulcstorage"


##############################Function Block#############################

def getListOfEERunningTasks():
	allEETasks = subprocess.Popen(["earthengine","task","list"],stdout=subprocess.PIPE).stdout.read().splitlines()
	incompleteEETasks = []
	for elementOfAllEETasks in allEETasks:
		if "COMPLETED" not in elementOfAllEETasks and "FAILED" not in elementOfAllEETasks and "CANCELLED" not in elementOfAllEETasks:
			#incompleteEETasks.append(elementOfAllEETasks.split(" ")[4])
			elementDataForEE = subprocess.Popen(["earthengine","task","info",elementOfAllEETasks.split(" ")[0]],stdout=subprocess.PIPE).stdout.read().splitlines()[3].split(": ")[1]
			incompleteEETasks.append(elementDataForEE)
	return incompleteEETasks

def getListOfAllNotDoneFiles(locationToCheck):
	allNotDoneFiles = subprocess.Popen(["find",locationToCheck,"-name","*.notDone.txt"], stdout=subprocess.PIPE).stdout.read()
	allNotDoneFiles = allNotDoneFiles.replace(".notDone.txt","")
	allNotDoneFilesList = allNotDoneFiles.splitlines()
	return allNotDoneFilesList

def getListOfTaskNames():
	if(os.path.exists(startedTaskListFileName)) :
		with open(startedTaskListFileName) as f:
			taskListNames = f.readlines()
		taskListNames = map(lambda s: s.strip(), taskListNames)	#Removes end of line characters
	else:
		taskListNames = []
	return taskListNames
###########################Function Block End############################


if len(sys.argv) == 1:
	print("No paramaters received. This script must be passed two paramaters to be run. To find"
		+ "out more please relaunch this script with the first paramater being help.")
	exit()


if sys.argv[1] == "help":
	print("Welcome to the ImageDownloadFromCloudStorage help menu." 
		+ "\nThe objective of this script is to syncronize files from the Google Coud to a local "
		+ "location. It works by getting a list of all tasks that were started by the system. Then"
		+ " getting a list of all images that have not been gathered yet, found by looking for their"
		+ " .notDone.txt file. It then gets a list of all files that are currently being run on the"
		+ " Google Earth Engine and filters them for unfinished files. Using this information, this"
		+ " script can determine what images have been processed by the Google Earth Engine and what"
		+ " still needs to be run. The following paramaters must be met for this script to run:"
		+ "\n1)Task list. Created by running the AssetMirrorScriptV2.py script(script that creates the tasks)"
		+ "\n2)LocalStorageLocationForDownloading. Should be the same as the one given to the AssetMirrorScriptV2.py script.")
	exit()

if len(sys.argv) != 3:
	print("Incorrect number of paramaters received. This script must be passed two paramaters to be run."
		+" To find ot more please relaunch this script with the first paramater being help.")
	exit()

startedTaskListFileName = sys.argv[1]
localStorageLocationForFiles = sys.argv[2]

listOfRunningTasks = getListOfEERunningTasks()
print(listOfRunningTasks)

taskListNames = getListOfTaskNames()


listOfNotDoneFiles = getListOfAllNotDoneFiles(localStorageLocationForFiles)
while len(listOfNotDoneFiles) > 0:
	for aNotDoneFile in listOfNotDoneFiles:
		imgName = aNotDoneFile.split("/")[-1]
		if aNotDoneFile.replace(localStorageLocationForFiles+"/","") in taskListNames:
			print(imgName + " has been added to be run")
			if imgName in listOfRunningTasks:
				print(imgName + " has been added but not run yet, skipping for now")
			else:
				print("image ready to be downloaded")
				print(aNotDoneFile.replace(localStorageLocationForFiles,CloudStorageBucketName))
				existenceCheck = subprocess.Popen(["gsutil","du",aNotDoneFile.replace(localStorageLocationForFiles,CloudStorageBucketName)],stdout=subprocess.PIPE).stdout.read()
				if len(existenceCheck) > 0:
					print("File found on cloud storage, downloading now")
					outputLocation = aNotDoneFile.replace(imgName,".")
					print(outputLocation)
					subprocess.Popen(["gsutil","cp","-r",aNotDoneFile.replace(localStorageLocationForFiles,CloudStorageBucketName),outputLocation],stdout=subprocess.PIPE).stdout.read()
					subprocess.Popen(["gsutil","rm","-r",aNotDoneFile.replace(localStorageLocationForFiles,CloudStorageBucketName)],stdout=subprocess.PIPE).stdout.read()
					os.remove(aNotDoneFile + ".notDone.txt")
				else:
					print("File not found on cloud storage")
		else:
			print("Image has not been run")
			print(aNotDoneFile.replace(localStorageLocationForFiles+"/",""))
	print("Waiting " + str(TimeToSleepBetweenRuns/60) + " minutes to see if there are any more images that can be downloaded")
	time.sleep(TimeToSleepBetweenRuns)

	#get new info for lists for next loop
	listOfNotDoneFiles = getListOfAllNotDoneFiles(localStorageLocationForFiles)
	listOfRunningTasks = getListOfEERunningTasks()
	taskListNames = getListOfTaskNames()

print("All not done files resolved. Run COMPLETED")