#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import os
from dotenv import load_dotenv

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()  # Loads variables from .env file

GALAXY_URL = os.getenv("GALAXY_URL")
API_KEY = os.getenv("GALAXY_API_KEY")
FILE_NAME = os.getenv("FILE_NAME", "biobhistory.fastq")  # Default value if not in .env
FILE_TYPE = os.getenv("FILE_TYPE", "fastqsanger")
NEW_LIBRARY_NAME = os.getenv("NEW_LIBRARY_NAME", "MyLibrary")
NEW_LIBRARY_DESC = os.getenv("NEW_LIBRARY_DESC", "Automatically created library via Bioblend")

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
# LIST EXISTING LIBRARIES
# ----------------------------
libraries = gi.libraries.get_libraries()

if not libraries:
    print("No libraries found. Creating a new library...")
    new_lib = gi.libraries.create_library(name=NEW_LIBRARY_NAME, description=NEW_LIBRARY_DESC)
    LIBRARY_ID = new_lib['id']
    print(f"Created library '{NEW_LIBRARY_NAME}' with ID: {LIBRARY_ID}")
else:
    # Use the first library if at least one exists
    LIBRARY_ID = libraries[0]['id']
    print(f"Using existing library: {libraries[0]['name']} (ID: {LIBRARY_ID})")

# ----------------------------
# UPLOAD FILE TO LIBRARY
# ----------------------------
print(f"\nUploading '{FILE_NAME}' to library ID {LIBRARY_ID}...")
uploaded = gi.libraries.upload_file_from_local_path(LIBRARY_ID, FILE_NAME, file_type=FILE_TYPE)
dataset_id = uploaded[0]['id']
print(f"File uploaded successfully! Dataset ID: {dataset_id}")

# ----------------------------
# VERIFY LIBRARY CONTENTS
# ----------------------------
contents = gi.libraries.show_library(LIBRARY_ID, contents=True)
print(f"\nContents of library ID {LIBRARY_ID}:")
for item in contents:
    print(f"- {item['name']} | Type: {item['type']} | ID: {item['id']}")

print("\n✅ Auto upload to library complete!")
