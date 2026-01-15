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

# =========================
# Core Logic (testable)
# =========================
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return Galaxy instance"""
    return GalaxyInstance(url=url, key=key)

def select_library(gi, library_name=DEFAULT_LIBRARY_NAME):
    """Select an existing library by name. Returns library ID or None"""
    for lib in gi.libraries.get_libraries():
        if lib["name"] == library_name:
            return lib["id"]
    return None

def upload_file_to_library(gi, library_id, file_name, file_type=FILE_TYPE):
    """Upload a file to a given library. Returns dataset ID"""
    return gi.libraries.upload_file_from_local_path(library_id, file_name, file_type)[0]["id"]

def perform_upload(gi, file_name=FILE_NAME, library_name=DEFAULT_LIBRARY_NAME, file_type=FILE_TYPE):
    """
    High-level workflow:
    - Check file exists
    - Select library
    - Upload file
    Returns: dataset_id, error_message (None if success)
    """
    if not os.path.exists(file_name):
        return None, f"Error: File '{file_name}' not found!"

    library_id = select_library(gi, library_name)
    if not library_id:
        return None, f"Error: Library '{library_name}' not found!"

    dataset_id = upload_file_to_library(gi, library_id, file_name, file_type)
    return dataset_id, None

# =========================
# CLI / main wrapper
# =========================
def main():
    gi = get_galaxy_instance()
    print("Connected to Galaxy.")

    dataset_id, error = perform_upload(gi)
    if error:
        print(error)
        return

    print(f"File uploaded successfully! Dataset ID: {dataset_id}")


if __name__ == "__main__":
    main()
