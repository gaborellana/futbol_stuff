import json, glob
from aux import *


event_files_path = "/home/gablinux/futbol_db/events/"
event_files = sorted(glob.glob(event_files_path + "*.json"))

shot_files_path = "/home/gablinux/futbol_db/shots_data/"
for e in event_files:
    shot_data = extractShotData(e)
    name = e.split("/")[-1].split(".")[0] + "_shot.json"
    with open(shot_files_path + name, "w") as f:
        json.dump(shot_data, f)

