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

train_dataloader[0]
# %%
