# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os, glob, json


#import statsbombpy as sb

# %%
cwd = os.getcwd()
print(cwd)


# %%

db_folder = "/home/gablinux/futbol_db/three-sixty/"
files = sorted(glob.glob(db_folder + "*.json"))


# %%
with open(files[0]) as json_file:
    events = json.load(json_file)



# %%

frames = []
for j in range(100):
    eventj = events[j]
    players=eventj["freeze_frame"]
    actor = []
    teammates = []
    rivals = []
    keeper = []
    for i in range(len(players)):
        if players[i]["actor"]:
            actor.append(players[i]["location"])
        elif players[i]["keeper"]:
            keeper.append(players[i]["location"])
        else:
            if players[i]["teammate"]:
                teammates.append(players[i]["location"])
            else:
                rivals.append(players[i]["location"])

    actor = np.array(actor)
    teammates = np.array(teammates)
    rivals = np.array(rivals)
    keeper = np.array(keeper)
    frames.append([actor, teammates, rivals, keeper])

# %%
frames_path = "/home/gablinux/futbol_db/frames/"

# %%

for j in range(len(frames)):
    frame = frames[j]
    actor = frame[0]
    teammates = frame[1]
    rivals = frame[2]
    keeper = frame[3]

    fig = plt.figure()
    plt.scatter(actor[:,0], actor[:,1], c="b")
    if teammates.shape != (0,):
        plt.scatter(teammates[:,0], teammates[:,1], c="g")
    if rivals.shape != (0,):
        plt.scatter(rivals[:,0], rivals[:,1], c="r")
    if keeper.shape != (0,):
        plt.scatter(keeper[:,0], keeper[:,1], c="m")
    plt.xlim(-5,125)
    plt.ylim(-5,125)
    plt.close(fig)

    fig.savefig(frames_path + "frame_{}.png".format(str(j)))




# %%
keeper.shape == (0,)

# %%
