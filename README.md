# GEEAssetDuplication
A set of scripts that can synchronize server side Google Earth Engine assets to local storage location. Please note this method uses the Google Cloud Storage in order to serve as an intermediate storage location for the GEE assets to be stored to before they can be downloaded to a local location.

# Requirements
The following packages must be installed for the project to work:

1)earthengine python API

2)gsutil

# How to use this project
This project is set up as two scripts that run in parallel. This was done during development to have one script upload to the Cloud Storage while the script for the download was being developed. Therefore both scripts will have to be run at the same time in order to work. There are two scripts to run, which are the two main scripts of this project:

1)AssetMirrorScriptV2.py: This script creates a local tree structure of the project with a temp text file representing the location of all images that are found in your GEE Assets. After this is done the system will make a list of all of the temp files and will create an export task for each of the images to be uplaoded from the GEE to Cloud Storage. Once a task is created, the asset path is saved into a locally created tasks file that is used to track which tasks have been started. An example of calling the script can be found below:

python AssetMirrorScriptV2.py users/alemlakes /Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete/


2)ImageDownloadFromCloudStorage.py This script takes files that have been uplaoded to the cloud storage and downloads them to the local file location set up by the AssetMirrorScriptV2.py script. Please note the script creates a folder of where the image was on the GEE Asset storage and stores the exported image within it, due to how some exported images are exported into multiple files. It uses the tasks file created by the mentioned script to determine what images should be searched for on the Cloud Storage, along with the bash command "earthengine task list". An example of calling the script can be found below:

python ImageDownloadFromCloudStorage.py tasks.txt /Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete/
