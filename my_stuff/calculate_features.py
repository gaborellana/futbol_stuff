"""
initially all the positions will be normalized to the actor's position

then nodes will be an encoding for actor, rival, teammate and keeper

edges are absolute distance to the actor and angle

in the basic implementation (just with positions of players and one frame), the
nodes will be very basic, although future implementations could add much more
complexity, such as field position, velocity, height, type of play, way to impact
the ball (header, left foot, right foot), etc

"""


"""
We will use one layer of convolution that will convolute over every single point, 
the convolution will be run on a graph where the others evaluated point is the 
top and ordering them from closest to farthest neighbors with some k parameter.

We will obtain some hidden state value for each player.

We then run a final convolution but just for the actor.

The output is pass through linear layers and run on logistic function to convert
it to probability.

"""

"""
other options to consider:
RBF
"""

# %%

import torch
import numpy as np
from dataset import ShotDataset, ShotLoader


# %%

training_data = ShotDataset()
train_dataloader = ShotLoader(training_data, batch_size=64, shuffle=True)

for batch in train_dataloader:
    break

# %%

def vectorize_locations(batch, device="cpu"):
    B = len(batch)
    L_max = max([1+len(b[1])+len(b[2])+len(b[3]) for b in batch])
    X = np.zeros([B, L_max, 2])
    L = np.zeros([B, L_max], dtype=np.int16)
    mask = np.zeros(L.shape)
    X[:] = -1 # positions with no players will be filled as -1
    #L[:] = -1 # labels with no players will be filled as -1
    target = np.array([b[4] for b in batch])

    # Build the batch
    for bi, b in enumerate(batch):
        x = np.expand_dims(np.array(b[0]), axis=0)
        #print(x.shape)
        L[bi,0] = 0
        mask[bi,0] = 1
        ik = 1 # index of the first player
        for j in range(1,4): # loop over teammates, rivals and keeper
            aux = np.array(b[j])
            #print(x.shape, aux.shape)
            x = np.concatenate((x, aux), 0)
            for _ in range(len(b[j])):
                L[bi,ik] = j
                mask[bi,ik] = 1
                ik += 1
        
        X[bi,0:x.shape[0],:] = x

    target = torch.from_numpy(target).to(dtype=torch.int8,device=device)
    X = torch.from_numpy(X).to(dtype=torch.float32, device=device)     
    L = torch.from_numpy(L).to(dtype=torch.int8, device=device)
    mask = torch.from_numpy(mask).to(dtype=torch.int8, device=device)
    return X, L, target, mask
"""
        perro = gato
        
        l = len(b['seq'])
        x_pad = np.pad(x, [[0,L_max-l], [0,0], [0,0]], 'constant', constant_values=(np.nan, ))
        X[i,:,:,:] = x_pad

        # Convert to labels
        indices = np.asarray([alphabet.index(a) for a in b['seq']], dtype=np.int32)
        if shuffle_fraction > 0.:
            idx_shuffle = shuffle_subset(l, shuffle_fraction)
            S[i, :l] = indices[idx_shuffle]
        else:
            S[i, :l] = indices

    # Mask
    isnan = np.isnan(X)
    mask = np.isfinite(np.sum(X,(2,3))).astype(np.float32)
    X[isnan] = 0.

    # Conversion
    S = torch.from_numpy(S).to(dtype=torch.long,device=device)
    X = torch.from_numpy(X).to(dtype=torch.float32, device=device)
    mask = torch.from_numpy(mask).to(dtype=torch.float32, device=device)
    return X, S, mask
"""
X, L, target, mask = vectorize_locations(batch)


# %%
L[0]

# %%
def test(batch):
    X, L, target, mask = vectorize_locations(batch)
    a = np.array([0,1,1,1,1,2,2,2,2,2,2,2,3,0,0,0,0,0,0,0])
    # check L[0] equals to a
    assert L[0].numpy().tolist() == a.tolist(), str(L[0]) + " different not equal to " + str(a)
    print("labels test passed")

    # check if the positions with 0 in L are zeros in mask +1
    for i in range(len(L)):
        assert np.sum(L[i].numpy() == 0) == np.sum(mask[i].numpy() == 0)+1, "number of -1 in L is not equal to number of zeros in mask"
    print("mask test passed")

test(batch)

# %%

class FeatCalc():
    def __init__(self, X, L, mask):
        self.hidden_size = 32
        self.k = 7
        self.embeddding_layer = torch.nn.Embedding(4, self.hidden_size)
        self.calc_features(X, L, target, mask)
        
    def calc_features(self, X, L, mask):
        
        Nodes = self.embeddding_layer(L)*mask
        dists, angles = self.calc_distances(X)
        Edges = torch.zeros(X.shape[0], X.shape[1], self.k, self.hidden_size)
        #for i in range(X.shape[0]):


    def calc_distances_angles(self, X, mask):
        # X: [batch, nodes, 2]
        # mask: [batch, nodes]
        # calculate distances
        dists = torch.cdist(X, X)
        #angles = torch.zeros(X.shape[0], X.shape[1], X.shape[1])
        nX = X / torch.norm(X, p=2, dim=-1, keepdim=True)
        # compute cosine of the angles using dot product
        angles = torch.einsum('bni,bmi->bnm', nX, nX)
        return dists, angles
    
    