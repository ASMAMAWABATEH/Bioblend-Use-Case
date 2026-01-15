# BioBlend/interactive_upload_to_library.py
from src.BioBlend.connect_to_galaxy import get_galaxy_instance
from typing import Tuple, Optional, List, Dict

GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

# =========================
# Core Logic (testable)
# =========================
def select_library(gi, library_name: str) -> Optional[Dict]:
    """Select an existing library by name. Returns dict if found, else None."""
    libraries = gi.libraries.get_libraries()
    for lib in libraries:
        if lib["name"] == library_name:
            return lib
    return None

def upload_file(gi, library_id: str, file_path: str, file_type: str = "auto") -> List[Dict]:
    """Upload a file to a given library."""
    return gi.libraries.upload_file_from_local_path(file_path, library_id, file_type=file_type)

def perform_upload(
    gi,
    library_name: str,
    file_path: str,
    file_type: str = "auto"
) -> Tuple[Optional[Dict], Optional[List[Dict]]]:
    """
    High-level wrapper: select library and upload file.
    Returns (library, upload_result) or (None, None) if library not found.
    """
    library = select_library(gi, library_name)
    if not library:
        return None, None
    result = upload_file(gi, library["id"], file_path, file_type=file_type)
    return library, result

def format_upload_result(library_name: str, file_path: str, result: List[Dict]) -> List[str]:
    """Format upload result for printing."""
    lines = [f"Uploading file '{file_path}' to library '{library_name}'..."]
    lines.append("Upload completed. Uploaded items:")
    for item in result:
        lines.append(f"- {item['name']} | ID: {item['id']} | Type: {item['file_ext']}")
    return lines

# =========================
# CLI / main wrapper
# =========================
def main():
    print("Connecting to Galaxy...")
    gi = get_galaxy_instance(url=GALAXY_URL, key=API_KEY)

    library_name = input("Enter the target library name: ").strip()
    file_path = input("Enter the file path to upload: ").strip()
    file_type = input("Enter file type (default 'auto'): ").strip() or "auto"

    library, result = perform_upload(gi, library_name, file_path, file_type=file_type)
    if not library:
        print(f"Library '{library_name}' not found.")
        return

    for line in format_upload_result(library_name, file_path, result):
        print(line)


if __name__ == "__main__":
    main()
