# GEEAssetDuplication
A set of scripts that can synchronize server side Google Earth Engine assets to local storage location. Please note this method uses the Google Cloud Storage in order to serve as an intermediate storage location for the GEE assets to be stored to before they can be downloaded to a local location.

# Requirements
The following packages must be installed for the project to work:

1)earthengine python API

2)gsutil

# How to use this project
This project is set up as two scripts that run in parallel. This was done during development to have one script upload to the Cloud Storage while the script
