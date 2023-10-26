import csv
import io
import os
import pickle

import magic
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Define your input and output CSV filenames
input_csv_filename = 'form.csv'
output_csv_filename = 'form_updated.csv'
input_csv_media_column = 'data-picture'
output_csv_media_column = 'data-picture-filename'
media_directory = './media'
google_api_credentials = 'credentials.json'

# Initialize the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, prompt the user to log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(google_api_credentials, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

drive_service = build('drive', 'v3', credentials=creds)

os.makedirs(os.path.dirname(media_directory), exist_ok=True)

# Function to download file
def download_file(file_id, file_name):
    file_path = os.path.join(media_directory, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        return

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    with open(file_path, "wb") as f:
        f.write(fh.getvalue())

# Open the CSV file for reading and writing
with open(input_csv_filename, 'r', newline='') as csvfile, \
        open(output_csv_filename, 'w', newline='') as output_csvfile:
    
    # CSV reader and writer
    reader = csv.DictReader(csvfile)
    input_fieldnames = reader.fieldnames  # Get the fieldnames from the input CSV

    # Insert the output_csv_media_column into the input_fieldnames list
    input_csv_media_column_index = input_fieldnames.index(input_csv_media_column)
    output_fieldnames = input_fieldnames.copy()
    output_fieldnames.insert(input_csv_media_column_index + 1, output_csv_media_column)
    
    writer = csv.DictWriter(output_csvfile, fieldnames=output_fieldnames)
    writer.writeheader()  # Write header to the output CSV
    
    # Create the media directory if it doesn't exist
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)
    
    for row in reader:
        # Extract the Google Drive ID from the link
        google_drive_id = row[input_csv_media_column].split('id=')[-1]
        download_link = f"https://drive.google.com/u/0/uc?id={google_drive_id}&export=download"

        file = drive_service.files().get(fileId=google_drive_id).execute()
        
        # Remove any slashes from past dir structure
        file_name = os.path.basename(file['name'])
        download_file(google_drive_id, file_name)
                
        updated_row = {field: row.get(field, '') for field in output_fieldnames}
        updated_row[output_csv_media_column] = file_name
        writer.writerow(updated_row)
        
        print(f"{file_name} downloaded (or already existed) and added to CSV.")

print("All media downloaded and CSV updated!")
