#Prgoram: AssetMirrorScript.py
#Programmer: Eric Davies
#Date: 18/5/2018
#Description: A script that copies assets from the earth engine to a local directory.
#Requirements:
#	1)Repository Name
#	2)Full path to sync directory

import ee
import sys
import subprocess
import os.path
import json
import time

TimeToSleepBetweenRuns = 200	#Number of seconds
MaximumNumberOfTasks = 20
CloudStorageBucketName = "bulcstorage"


############################Function Block#######################
def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

def getNumberOfEERunningTasks():
    allEETasks = subprocess.Popen(["earthengine","task","list"],stdout=subprocess.PIPE).stdout.read().splitlines()
    incompleteEETasks = []
    for elementOfAllEETasks in allEETasks:
        if "COMPLETED" not in elementOfAllEETasks and "FAILED" not in elementOfAllEETasks and "CANCELLED" not in elementOfAllEETasks:
            incompleteEETasks.append(elementOfAllEETasks.split(" ")[2])
    return len(incompleteEETasks)
#######################Function Block End########################


#Program Start

ALLDONE = "allDone.done.txt"


#################Input Handling##############
repo = sys.argv[1]
syncRepository = sys.argv[2]
###############Input Handling End############


##############Make Start Folders#############
repoSplit = repo.split('/')
print(repoSplit)

folderPath = syncRepository + repoSplit[0]
print(folderPath)
if(not os.path.exists(folderPath)):
	os.makedirs(folderPath)
else:
	print(folderPath +" file already exists")

for x in xrange(1,len(repoSplit)):
	folderPath += "/" + repoSplit[x]
	print(folderPath)
	if(not os.path.exists(folderPath)):
		os.makedirs(folderPath)
	else:
		print(folderPath + " file already exists")
###########Make Starting Folders End##########


###########Make .notDone.txt Files#############
print("Checking if all notDone files created:" + folderPath + "/" + ALLDONE)
if(not os.path.exists(folderPath + "/" + ALLDONE)):
	print("Not all not done files created, please run CreateNotDoneFiles before running this file.")
	sys.exit()
else:
    print("all notDone files created")
###########End Make .notDone.txt Files##########


ee.Initialize()

###########Run through all notDones and attempt to upload to Google Drive##########

#Get list of images that have had tasks already started for them. Does not account for errors
if(os.path.exists("tasks.txt")) :
	with open("tasks.txt") as f:
		content = f.readlines()
	content = map(lambda s: s.strip(), content)	#Removes end of line characters
else:
	content = []

#Opens tasks file to write into, not sure if this is proper with the file reading component but seems to work
taskFile = open("tasks.txt","a+")

allNoteDoneFiles = subprocess.Popen(["find",syncRepository + "/" + repo,"-name","*.notDone.txt"], stdout=subprocess.PIPE).stdout.read()
allNoteDoneFiles = allNoteDoneFiles.replace(".notDone.txt","").replace(syncRepository+"/","")
allNoteDoneFilesList = allNoteDoneFiles.splitlines()

#Wait for the number of running tasks to be less than the MaximumNumberOfTasks
while (getNumberOfEERunningTasks() > MaximumNumberOfTasks):
    print("Too many tasks running, waiting "+ str(TimeToSleepBetweenRuns/60) +" minutes before continuing")
    time.sleep(TimeToSleepBetweenRuns)

#Loop over all not done files
for aNoteDoneFileName in allNoteDoneFilesList:
	try:
		print(aNoteDoneFileName)
		name = aNoteDoneFileName.split("/")[-1]
		print(name)

		#Check if tasks started for item
		if aNoteDoneFileName in content:
			print("Task already done")
		else:
			print("Task not completed")
			img = ee.Image(aNoteDoneFileName)
			exportName = aNoteDoneFileName.split('/')[-1]
			imgScale = img.projection().nominalScale().round().getInfo()

			task = ee.batch.Export.image.toCloudStorage(
				image = img,
				scale = imgScale,
				bucket = CloudStorageBucketName,
				description = exportName,
				fileNamePrefix = aNoteDoneFileName +"/"+ exportName,
				maxPixels = 1000000000000,
				)
			print(aNoteDoneFileName + "/" + exportName)
			taskFile = open("tasks.txt","a+")
			taskFile.write(aNoteDoneFileName + "\n")
			taskFile.close()
			print("Start Export")
			task.start()
			print(task.status())
			while (getNumberOfEERunningTasks() > MaximumNumberOfTasks):
				print("Too many tasks running, waiting "+ str(TimeToSleepBetweenRuns/60) +" minutes before continuing")
				time.sleep(TimeToSleepBetweenRuns)
	except KeyboardInterrupt:
		sys.exit()
	except:
		print("Error with file")
    #wait to see if the number of running tasks is less than 50

	

#########Run through all notDones End###############


print("All tasks launched")
########EOF########
