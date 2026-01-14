# src/BioBlend/view_data_library.py
from bioblend.galaxy import GalaxyInstance

GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

# =========================
# Core Logic (testable)
# =========================
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """Create and return a Galaxy instance"""
    return GalaxyInstance(url=url, key=key)

def list_libraries(gi):
    """Return Galaxy data libraries with their datasets."""
    libraries = gi.libraries.get_libraries()
    results = []

    for lib in libraries:
        lib_details = gi.libraries.show_library(lib["id"])
        results.append({
            "id": lib["id"],
            "name": lib["name"],
            "description": lib_details.get("description", ""),
            "datasets": lib_details.get("datasets", []),
        })

    return results

def format_libraries_output(libraries):
    """Return a list of strings for CLI display"""
    lines = []
    for lib in libraries:
        lines.append(f"Library: {lib['name']} | Description: {lib['description']}")
        if lib["datasets"]:
            lines.append("  Contents:")
            for d in lib["datasets"]:
                lines.append(f"    - {d['name']} | Type: {d.get('type', 'unknown')} | ID: {d['id']}")
        else:
            lines.append("  (No datasets)")
        lines.append("-" * 40)
    return lines

# =========================
# CLI / main wrapper
# =========================
def main():
    gi = get_galaxy_instance()
    libraries = list_libraries(gi)
    for line in format_libraries_output(libraries):
        print(line)

if __name__ == "__main__":
    main()
