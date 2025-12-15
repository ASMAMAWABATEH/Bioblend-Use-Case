#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"       # Change if needed
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"              # Replace with your Galaxy API key
LIBRARY_ID = "replace_with_actual_library_id"  # Replace with a real library ID
FILE_NAME = "biobhistory.fastq"            # File to upload
FILE_TYPE = "fastqsanger"                  # Galaxy dataset type

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# CHECK FILE
# ----------------------------
if not os.path.exists(FILE_NAME):
    print(f"Error: File '{FILE_NAME}' not found!")
    exit(1)

# ----------------------------
# UPLOAD FILE TO DATA LIBRARY
# ----------------------------
if LIBRARY_ID == "replace_with_actual_library_id":
    print("Error: Please set LIBRARY_ID to a valid library ID before running the script.")
    exit(1)

print(f"Uploading '{FILE_NAME}' to library ID {LIBRARY_ID}...")
# Correct method: first positional arg = library_id, second = file path
uploaded = gi.libraries.upload_file_from_local_path(LIBRARY_ID, FILE_NAME, file_type=FILE_TYPE)
dataset_id = uploaded[0]['id']
print(f"File uploaded successfully! Dataset ID: {dataset_id}")

# ----------------------------
# VERIFY LIBRARY CONTENTS
# ----------------------------
contents = gi.libraries.get_library_contents(LIBRARY_ID)
print(f"\nContents of library ID {LIBRARY_ID}:")
for item in contents:
    print(f"- {item['name']} | Type: {item['type']} | ID: {item['id']}")

print("\nDone ✅ Data library upload complete!")
