import csv
import os
import requests
import magic

# Define your input and output CSV filenames
input_csv_filename = 'form.csv'
output_csv_filename = 'form_updated.csv'
input_csv_media_column = 'data-picture'
output_csv_media_column = 'data-picture-filename'
media_directory = './media'

# Function to determine file extension from the MIME type
def get_extension_from_mime(mime_type):
    mime_to_extension = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/tiff': '.tif',
        'image/webp': '.webp',
        # ... add more MIME types as needed
    }
    return mime_to_extension.get(mime_type, '.unknown')

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
        download_link = f"https://drive.google.com/uc?export=download&id={google_drive_id}"
        
        # Determine file extension
        response = requests.head(download_link)
        mime_type = response.headers.get('Content-Type')
        file_extension = get_extension_from_mime(mime_type)
        media_filename = f"{google_drive_id}{file_extension}"
        
        media_path = os.path.join(media_directory, media_filename)
        
        # Download the media only if it doesn't exist
        if not os.path.exists(media_path):
            response = requests.get(download_link)
            with open(media_path, 'wb') as media_file:
                media_file.write(response.content)
            
            # Determine file extension
            mime_type = magic.from_file(media_path, mime=True)
            file_extension = get_extension_from_mime(mime_type)
            if file_extension == '.unknown':
                os.remove(media_path)  # remove the file with unknown extension
            else:
                # rename the file with the correct extension
                new_media_path = os.path.join(media_directory, f"{google_drive_id}{file_extension}")
                os.rename(media_path, new_media_path)
                media_path = new_media_path
                media_filename = f"{google_drive_id}{file_extension}"
        else:
            print(f"File {media_filename} already exists. Skipping download.")
                
        updated_row = {field: row.get(field, '') for field in output_fieldnames}
        updated_row[output_csv_media_column] = media_filename
        writer.writerow(updated_row)
        
        print(f"Downloaded {media_filename} and updated the CSV.")

print("All media downloaded and CSV updated!")
