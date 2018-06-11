#Program: CreateNotDoneFiles.py
#Programmer: Eric Davies
#Date: 8/6/2018
#Description: A script that generates the folder structure of the Earth Engine Asset repository in 
#   a local location. It creates not done files in the place for each of the actual files on the
#   EE Asset repository. These not done files are used for later components.

import subprocess
import sys
import os.path
import json


####################################Function Block################################
def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

##################################Function Block End##############################

ALLDONE = "allDone.done.txt"

repo = sys.argv[1]
syncRepository = sys.argv[2]

repoSplit = repo.split('/')
folderPath = syncRepository + repoSplit[0]

##############Make Start Folders#############
repoSplit = repo.split('/')
print(repoSplit)

folderPath = syncRepository + repoSplit[0]
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


print("Checking if all notDone files created:" + folderPath + "/" + ALLDONE)
if(not os.path.exists(folderPath + "/" + ALLDONE)):

    allFilesAndDirs = subprocess.Popen(["earthengine","ls","-r", repo], stdout=subprocess.PIPE)
    #allFilesAndDirs = subprocess.Popen(["cat","./output.txt"],stdout=subprocess.PIPE)
    allObjects = allFilesAndDirs.stdout.read().splitlines()

    for i in allObjects:
        itemInfo = subprocess.Popen(["earthengine","asset","info",i],stdout=subprocess.PIPE).stdout.read()
        itemJson = json.loads(itemInfo)
        print(itemJson)
        if(itemJson['type'] == 'Folder'):
            print(itemJson['id'] + " Folder")
            if(not os.path.exists(syncRepository + "/" + itemJson['id'])):
                os.makedirs(syncRepository + "/" + itemJson['id'])
        else:
            print(itemJson['id'] + " Not Folder")
            if(not os.path.exists(syncRepository + "/" + itemJson['id'] + ".notDone.txt")):
                touch(syncRepository + "/" + itemJson['id']+ ".notDone.txt")

    touch(folderPath+"/" + ALLDONE)
else:
    print("all notDone files created")