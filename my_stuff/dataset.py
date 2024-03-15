import os
from torch.utils.data import Dataset
from glob import glob
from my_stuff.utils import open_json

class ShotDataset(Dataset):
    def __init__(self, shots_file = "/home/gablinux/futbol_db/shots_data/"):
        self.db = open_json(shots_file)

    def __len__(self):
        return len(self.db)

    def __getitem__(self, idx):
        # shot = [position_actor, [teammates], [rivals], [keeper], goal]
        pos_actor = self.db[idx][0]
        teammates = self.db[idx][1]
        rivals = self.db[idx][2]
        keeper = self.db[idx][3]
        goal = self.db[idx][4]
        return pos_actor, teammates, rivals, keeper, goal