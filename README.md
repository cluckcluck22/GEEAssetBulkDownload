# GEEAssetBulkDownload
A set of scripts that can synchronize server side Google Earth Engine assets to local storage location. Please note this method uses the Google Cloud Storage in order to serve as an intermediate storage location for the GEE assets to be stored to before they can be downloaded to a local location.

# Requirements
The following packages must be installed for the project to work:

1)earthengine python API

2)gsutil

The machine the code is running on must also be a Linux or Unix machine, as the script relys on some command line calls to work.

# How to use this project
This project is set up as two scripts that run in parallel. This was done during development to have one script upload to the Cloud Storage while the script for the download was being developed. Therefore both scripts will have to be run at the same time in order to work. There are two scripts to run, which are the two main scripts of this project:

1)CreateNotDoneFiles.py: This script creates a folder tree structure of all files found on your GEE Asset folder and creates a not done file in the local file structure when an image is found on the GEE. The not done file will be created in the same location in the folder tree and is used to keep track of what images have been downloaded locally and which ones have not been. An example call can be seen below:

python CreateNotDoneFilesStep1.py users/alemlakes /Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete/

2)AssetMirrorScriptV2.py: The script makes a list of all of the temp files and will create an export task for each of the images to be uplaoded from the GEE to Cloud Storage. Once a task is created, the asset path is saved into a locally created tasks file that is used to track which tasks have been started. The script has options to modify the max number of tasks to try and export, along with the amount of seconds to wait between each upload attempt. Please note that you will need to change the bucket name for this script to work for you. An example of calling the script can be found below:

python AssetMirrorScriptStep2.py users/alemlakes /Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete/


3)ImageDownloadFromCloudStorage.py This script takes files that have been uplaoded to the cloud storage and downloads them to the local file location set up by the AssetMirrorScriptV2.py script. Please note the script creates a folder of where the image was on the GEE Asset storage and stores the exported image within it, due to how some exported images are exported into multiple files. It uses the tasks file created by the mentioned script to determine what images should be searched for on the Cloud Storage, along with the bash command "earthengine task list". Please note you will need to change the cloud storage bucket variable to one of your own for this to work. An example of calling the script can be found below:

python ImageDownloadFromCloudStorageStep3.py tasks.txt /Volumes/Big-Cloud-Work/GoogleDrives/alem.lakes/0.3.AssetMirrorComplete/


Optional)CheckForDownloadProgressStep4.py: This script is designed to allow for a user to check what files are missing from the local machine. It does so by pulling a current list of the Asset tree from the GEE, checking what objects are missing, and then creating four result files in the current working directory that store the valid files and folders along with the invalid ones. Please note that if any files are being uploaded to the GEE during the running of this project, they will be reported as invalid.
