# src/BioBlend/upload_to_library.py
import os
from bioblend.galaxy import GalaxyInstance

# --------------------------------------------------------------
# Configuration
# --------------------------------------------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"
DEFAULT_LIBRARY_NAME = "MyLibrary"
FILE_NAME = "bioblend_history.fastq"
FILE_TYPE = "fastqsanger"
# --------------------------------------------------------------

def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return Galaxy instance"""
    return GalaxyInstance(url=url, key=key)

def select_library(gi, library_name=DEFAULT_LIBRARY_NAME):
    """Select an existing library by name"""
    libraries = gi.libraries.get_libraries()
    for lib in libraries:
        if lib["name"] == library_name:
            return lib["id"]
    return None

def upload_file_to_library(gi, library_id, file_name, file_type=FILE_TYPE):
    """Upload a file to a given library"""
    return gi.libraries.upload_file_from_local_path(library_id, file_name, file_type)[0]["id"]

def main():
    """Main execution"""
    if not os.path.exists(FILE_NAME):
        print(f"Error: File '{FILE_NAME}' not found!")
        return

    gi = get_galaxy_instance()
    print("Connected to Galaxy.")

    library_id = select_library(gi)
    if not library_id:
        print(f"Error: Library '{DEFAULT_LIBRARY_NAME}' not found!")
        return

    dataset_id = upload_file_to_library(gi, library_id, FILE_NAME)
    print(f"File uploaded successfully! Dataset ID: {dataset_id}")

if __name__ == "__main__":
    main()
