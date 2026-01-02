# BioBlend/auto_upload_to_library.py
import os
from bioblend.galaxy import GalaxyInstance
from dotenv import load_dotenv

def get_env_variables():
    """Load environment variables with defaults"""
    load_dotenv()
    return {
        "GALAXY_URL": os.getenv("GALAXY_URL", "http://localhost:8080"),
        "API_KEY": os.getenv("GALAXY_API_KEY", "b8ba458fe9b1c919040db8288c56ed06"),
        "FILE_NAME": os.getenv("FILE_NAME", "bioblend_history.fastq"),
        "FILE_TYPE": os.getenv("FILE_TYPE", "fastqsanger"),
        "NEW_LIBRARY_NAME": os.getenv("NEW_LIBRARY_NAME", "MyLibrary"),
        "NEW_LIBRARY_DESC": os.getenv(
            "NEW_LIBRARY_DESC",
            "Automatically created library via Bioblend"
        )
    }

def connect_galaxy(url, key):
    """Return a GalaxyInstance"""
    return GalaxyInstance(url=url, key=key)

def select_or_create_library(gi, library_name, library_desc):
    """Select existing library or create a new one"""
    libraries = gi.libraries.get_libraries()
    if not libraries:
        new_lib = gi.libraries.create_library(name=library_name, description=library_desc)
        return new_lib["id"]
    return libraries[0]["id"]

def upload_file(gi, library_id, file_name, file_type):
    """Upload a file to the specified library"""
    return gi.libraries.upload_file_from_local_path(library_id, file_name, file_type)[0]["id"]

def show_library_contents(gi, library_id):
    """Return a structured list of library contents"""
    contents = gi.libraries.show_library(library_id, contents=True)
    return [(item["name"], item["type"], item["id"]) for item in contents]

def main():
    env = get_env_variables()

    if not os.path.exists(env["FILE_NAME"]):
        print(f"Error: File '{env['FILE_NAME']}' not found!")
        return

    gi = connect_galaxy(env["GALAXY_URL"], env["API_KEY"])
    print("Connected to Galaxy.")

    library_id = select_or_create_library(gi, env["NEW_LIBRARY_NAME"], env["NEW_LIBRARY_DESC"])
    print(f"Using library ID: {library_id}")

    dataset_id = upload_file(gi, library_id, env["FILE_NAME"], env["FILE_TYPE"])
    print(f"File uploaded successfully! Dataset ID: {dataset_id}")

    contents = show_library_contents(gi, library_id)
    print("\nLibrary contents:")
    for name, type_, id_ in contents:
        print(f"- {name} | Type: {type_} | ID: {id_}")

if __name__ == "__main__":
    main()
