# Download gdrive media from csv

This is a Python script that will scrape all media from a column with Google Drive links from an input CSV, and add the filenames to a new column in an output CSV.

The script currently assumes that Google Drive links are in the following format `https://drive.google.com/open?id=<file_id>`, and that the file sharing permissions are set that anyone with the link can open the file.
