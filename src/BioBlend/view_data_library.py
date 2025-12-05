#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
GALAXY_URL = "http://localhost:8080"  # Change if needed
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"          # Replace with your Galaxy API key
DOWNLOAD_DATASETS = False              # Set True if you want to download datasets

# ----------------------------
# CONNECT TO GALAXY
# ----------------------------
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
print("Connected to Galaxy.")

# ----------------------------
# LIST DATA LIBRARIES
# ----------------------------
libraries = gi.libraries.get_libraries()
print(f"\nFound {len(libraries)} data libraries:\n")

for lib in libraries:
    print(f"- {lib['name']} | ID: {lib['id']} | Description: {lib.get('description', 'No description')}")

# ----------------------------
# VIEW CONTENTS OF EACH LIBRARY
# ----------------------------
for lib in libraries:
    print(f"\nContents of library: {lib['name']} (ID: {lib['id']})")
    contents = gi.libraries.get_library_contents(lib['id'])
    if not contents:
        print("  (Library is empty)")
    for item in contents:
        print(f"  - {item['name']} | Type: {item['type']} | ID: {item['id']}")

        # Optional: download datasets
        if DOWNLOAD_DATASETS and item['type'] == "file":
            file_path = gi.libraries.download_dataset(
                item['id'],
                file_path=".",  # current directory
                use_default_filename=True
            )
            print(f"    -> Dataset downloaded to: {file_path}")

print("\nDone ✅ Data libraries viewed successfully!")
