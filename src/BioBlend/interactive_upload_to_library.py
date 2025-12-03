#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"   # Change if needed
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"          # Replace with your Galaxy API key
FILE_NAME = "biobhistory.fastq"        # File to upload
FILE_TYPE = "fastqsanger"              # Galaxy dataset type

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.\n")

# ----------------------------
# LIST DATA LIBRARIES
# ----------------------------
libraries = gi.libraries.get_libraries()
if not libraries:
    print("No libraries found on the server!")
    exit(1)

print("Available libraries:")
for i, lib in enumerate(libraries, 1):
    print(f"{i}. {lib['name']} | ID: {lib['id']}")

# ----------------------------
# SELECT LIBRARY INTERACTIVELY
# ----------------------------
choice = input("\nEnter the number of the library to upload to: ")
try:
    choice = int(choice)
    if choice < 1 or choice > len(libraries):
        raise ValueError
except ValueError:
    print("Invalid selection!")
    exit(1)

LIBRARY_ID = libraries[choice - 1]['id']
print(f"\nSelected library: {libraries[choice - 1]['name']} (ID: {LIBRARY_ID})")

# ----------------------------
# CHECK FILE
# ----------------------------
if not os.path.exists(FILE_NAME):
    print(f"Error: File '{FILE_NAME}' not found!")
    exit(1)

# ----------------------------
# UPLOAD FILE TO LIBRARY
# ----------------------------
print(f"\nUploading '{FILE_NAME}' to library '{libraries[choice - 1]['name']}'...")
uploaded = gi.libraries.upload_file_from_local_path(LIBRARY_ID, FILE_NAME, file_type=FILE_TYPE)
dataset_id = uploaded[0]['id']
print(f"File uploaded successfully! Dataset ID: {dataset_id}")

# ----------------------------
# VERIFY LIBRARY CONTENTS
# ----------------------------
contents = gi.libraries.get_library_contents(LIBRARY_ID)
print(f"\nContents of library '{libraries[choice - 1]['name']}':")
for item in contents:
    print(f"- {item['name']} | Type: {item['type']} | ID: {item['id']}")

print("\n✅ Data library upload complete!")

