from bioblend.galaxy import GalaxyInstance

GI_URL = "http://localhost:8080"
GI_KEY = "b8ba458fe9b1c919040db8288c56ed06"

gi = None  # Do not create instance at import time

def get_gi():
    """
    Return a GalaxyInstance, create it if it doesn't exist yet.
    Lazy initialization avoids connecting at import time.
    """
    global gi
    if gi is None:
        gi = GalaxyInstance(url=GI_URL, key=GI_KEY)
        print("Connected to Galaxy!")
        print("Galaxy version:", gi.config.get_version())
    return gi

def main():
    gi_instance = get_gi()
    # You can now use gi_instance for workflows, uploads, tools, etc.

if __name__ == "__main__":
    main()
