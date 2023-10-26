# Google Drive Media Downloader and CSV Updater


This Python script is designed to download media files from Google Drive and update a CSV file with the filenames of the downloaded files.

**How it works**

1. The script reads a CSV file and identifies a column that contains Google Drive links to media files.

2. It authenticates with the Google Drive API using OAuth 2.0. If a token is already available and valid, it uses that. Otherwise, it prompts the user to log in and authorizes the application.

3. The script then iterates over each row in the CSV file, extracts the Google Drive ID from the link, and downloads the corresponding file. If the file already exists in the specified directory, it skips the download.

4. After downloading the file, it updates the row in the CSV with the filename of the downloaded file and writes the updated row to a new CSV file.

5. The process repeats until all rows in the CSV file have been processed. The script then prints a message indicating that all media files have been downloaded and the CSV file has been updated.
   
**Requirements**

This script requires the following Python libraries:

- csv
- io
- os
- pickle
- magic
- requests
- google_auth_oauthlib
- google.auth.transport.requests
- googleapiclient.discovery
- googleapiclient.http

Before running the script, make sure to define your input and output CSV filenames and columns, and replace 'credentials.json' with the path to your Google API credentials file.
