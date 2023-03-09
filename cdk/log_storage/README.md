# Makerspace Log Usage 

This folder contain all relevant code and objects needed for the storage of Makerspace's Logs and their use in Quicksight. Makerspace collects data on Prints, Projects, and more through their Google Form which writes to Google Sheets. This Log contains data that can be utilized in Quicksight, but there is currently not a direct way to link Quicksight to Google Sheets. We can store that data as a csv into an S3 bucket for Quicksight to pull from.

## Folder Structure
1. \_\_init\_\_.py - Cloudformation stack that contains an S3 bucket that should store any Log files (in .csv format)
2. s3_manifest/s3logmanifest.json - This manifest JSON format is needed when connecting Quicksight to a new S3 data source
3. apps_script_code/ - Contains Google Apps Script for uploading Log data from Google Sheets to S3


## Script Usage
- The apps script can only be used in a Google Apps Script Project (https://script.google.com/home/start)
- The account running this script must have Google access to Makerspace's Log (in Google Sheets)
- Edit sheetId and sheetName variables with the Log's data
- Need to edit file to include an Access key and Secret Access key from an IAM User with access to your S3 bucket

## Quicksight Integration with S3

1. First you must allow the Quicksight account to have access to your specific S3 bucket (Found in Security Options in "Manage Quicksight" option in Quicksight console)
2. If the dataset does not already exist, add a new dataset from S3
3. Upload the s3logmanifest.json file when prompted (make sure you adjust the bucket and file names first)
4. Once successful, you can set a Refresh schedule on your dataset to pull new data from the csv file in S3 (note any new log uploads to S3 should have the same file name)
5. Now, you should be able to add the log dataset to a Quicksight Analysis
