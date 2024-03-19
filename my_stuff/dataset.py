import numpy as np
from torch.utils.data import Dataset
from utils import open_json

class ShotDataset(Dataset):
    def __init__(self, shots_file = "/home/gablinux/futbol_db/shots_data/shots_db.json"):
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


class ShotLoader():
    def __init__(self, dataset, batch_size=100, shuffle=True):
        self.dataset = dataset
        self.size = len(dataset)
        self.batch_size = batch_size
        idxs = np.arange(len(self.dataset))
        np.random.shuffle(idxs)
        
        batches, batch = [], []
        for ix in idxs:
            current_batch_size = len(batch)
            if current_batch_size == self.batch_size:
                batches.append(batch)
                batch = []
            else:
                batch.append(self.dataset[ix])
                
        if len(batch) > 0:
            batches.append(batch)
        self.batches = batches

    def __len__(self):
        return len(self.batches)

    def __iter__(self):
        np.random.shuffle(self.batches)
        for batch in self.batches:
            yield batch


#def test():
#    training_data = ShotDataset()
#    train_dataloader = ShotLoader(training_data, batch_size=64, shuffle=True)
#    for batch in train_dataloader:
#        break
#    assert len(batch)==64, "size of batch is wrong"
#test()