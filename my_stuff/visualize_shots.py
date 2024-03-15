# %%
import matplotlib.pyplot as plt
import numpy as np
import glob
from my_stuff.utils import open_json

# %%

files = sorted(glob.glob("/home/gablinux/futbol_db/shots_data/*.json"))

j = 0

shots = open_json(files[j])
print(files[j])

# %%
# = shots = [position_actor, [teammates], [rivals], [keeper], goal]
for shot in shots:
    #shot = shots[shoti]
    fig = plt.figure()
    plt.scatter(shot[0][0], shot[0][1], color="b")
    for ti in range(len(shot[1])):
        plt.scatter(shot[1][ti][0], shot[1][ti][1], color="g")
    for ri in range(len(shot[2])):
        plt.scatter(shot[2][ri][0], shot[2][ri][1], color="r")
    for ri in range(len(shot[3])):
        plt.scatter(shot[3][ri][0], shot[3][ri][1], color="m")
    plt.title(shot[4])
    plt.show()

# %%
