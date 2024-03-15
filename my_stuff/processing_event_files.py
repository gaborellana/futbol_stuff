import json, glob
from my_stuff.utils import *


event_files_path = "/home/gablinux/futbol_db/events/"
event_files = sorted(glob.glob(event_files_path + "*.json"))

shots_db_file = "/home/gablinux/futbol_db/shots_data/shots_db.json"

shot_data = []
for e in event_files:
    shot_data = shot_data + extractShotData(e)
    
with open(shots_db_file, "w") as f:
    json.dump(shot_data, f)

