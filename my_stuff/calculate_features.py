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
    L[:] = -1 # positions with no players will be found as -1
    target = np.array([b[4] for b in batch])

    # Build the batch
    for bi, b in enumerate(batch):
        x = np.expand_dims(np.array(b[0]), axis=0)
        #print(x.shape)
        L[0] = 0
        ik = 0
        for j in range(1,4):
            aux = np.array(b[j])
            print(x.shape, aux.shape)
            x = np.concatenate((x, aux), 0)
            for _ in b[j]:
                j =+ 1
                L[ik] = j
                
        X[bi,0:x.shape[0],:] = X

            
        return X
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

X = vectorize_locations(batch)
# %%
len(batch)

# %%
