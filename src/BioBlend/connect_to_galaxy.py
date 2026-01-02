from bioblend.galaxy import GalaxyInstance

# ----------------------------
# Configuration
# ----------------------------
GALAXY_URL = "http://localhost:8080"
API_KEY = "b8ba458fe9b1c919040db8288c56ed06"

# ----------------------------
def get_galaxy_instance(url=GALAXY_URL, key=API_KEY):
    """
    Create and return a GalaxyInstance
    """
    return GalaxyInstance(url=url, key=key)

def test_connection(gi):
    """
    Test connection by fetching user info or version
    """
    try:
        version = gi.gi_version
        return {"status": "ok", "version": version}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    print("Connecting to Galaxy...")
    gi = get_galaxy_instance()

    result = test_connection(gi)
    if result["status"] == "ok":
        print(f"Connected successfully! Galaxy version: {result['version']}")
    else:
        print(f"Connection failed: {result['message']}")

if __name__ == "__main__":
    main()
