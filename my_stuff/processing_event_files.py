import glob
from utils import *
import pandas as pd
from data_extraction import ShotDataExtractor


event_files_path = "/home/gablinux/futbol_db/events/"
event_files = sorted(glob.glob(event_files_path + "*.json"))

shots_db_file = "/home/gablinux/futbol_db/shots_data/shots_db.json"

extractor = ShotDataExtractor()
for e in event_files:
    extractor.extractShotData(e)

df = pd.DataFrame(extractor.get_dict())
    
df.to_json(shots_db_file, orient='records')

