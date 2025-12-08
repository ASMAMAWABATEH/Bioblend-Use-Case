
from bioblend.galaxy import GalaxyInstance

GI_URL = "http://localhost:8080"
GI_KEY = "b8ba458fe9b1c919040db8288c56ed06"

gi = GalaxyInstance(url=GI_URL, key=GI_KEY)

print("Connected to Galaxy!")
print("Galaxy version:", gi.config.get_version())
