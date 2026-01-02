# BioBlend/interactive_upload_to_library.py
from BioBlend.connect_to_galaxy import get_galaxy_instance

# Default configuration
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

def select_library(gi, library_name):
    """
    Select an existing library by name.
    Returns the library dict if found, otherwise None.
    """
    libraries = gi.libraries.get_libraries()
    for lib in libraries:
        if lib["name"] == library_name:
            return lib
    return None

def upload_file(gi, library_id, file_path, file_type="auto"):
    """
    Upload a file to a given library.
    """
    upload_result = gi.libraries.upload_file_from_local_path(
        file_path,
        library_id,
        file_type=file_type
    )
    return upload_result

def main():
    print("Connecting to Galaxy...")
    gi = get_galaxy_instance(url=GALAXY_URL, key=API_KEY)

    library_name = input("Enter the target library name: ").strip()
    library = select_library(gi, library_name)
    if not library:
        print(f"Library '{library_name}' not found.")
        return

    file_path = input("Enter the file path to upload: ").strip()
    file_type = input("Enter file type (default 'auto'): ").strip() or "auto"

    print(f"Uploading file '{file_path}' to library '{library_name}'...")
    result = upload_file(gi, library["id"], file_path, file_type=file_type)
    print("Upload completed. Uploaded items:")
    for item in result:
        print(f"- {item['name']} | ID: {item['id']} | Type: {item['file_ext']}")

if __name__ == "__main__":
    main()
