from bioblend.galaxy import GalaxyInstance

GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

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


def main():
    gi = get_galaxy_instance()
    libraries = list_libraries(gi)

    for lib in libraries:
        print(f"Library: {lib['name']} | Description: {lib['description']}")
        if lib["contents"]:
            print("  Contents:")
            for item in lib["contents"]:
                print(f"    - {item['name']} | Type: {item['type']} | ID: {item['id']}")
        else:
            print("  (No contents)")
        print("-" * 40)

if __name__ == "__main__":
    main()
