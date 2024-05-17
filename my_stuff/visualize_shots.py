# %%
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def visualize_shot(goalsdf, i):
    field_img = mpimg.imread("futbol_field.jpg")
    #left-up corner: 38,24
    #right-up corner: 510,24
    #right-down corner: 510,339
    #left-down corner: 38,339
    # linear conversion: x = 38 + (510-38)*(x_pos/120)
    #                    y = 24 - (339-24)*(y_pos/80)

    colors = ['red', 'magenta', 'blue', 'yellow']

    roles = goalsdf["roles"].to_list()
    positions = goalsdf["positions"].to_list()
    predxg = goalsdf["predxg"].to_list()
    gameid = goalsdf["gameid"].to_list()
    posi = np.array(positions[i])
    posi[:, 0] = 38 + (510-38)*(posi[:, 0]/120)
    posi[:, 1] = 24 + (339-24)*(posi[:, 1]/80)
    roli = roles[i]
    coli = [colors[roli[j]] for j in range(len(roli))]
    plt.imshow(field_img)
    plt.scatter(posi[:, 0], posi[:, 1], color=coli)
    plt.title("calc_xG=" + str(predxg[i]) + " -- gameid=" + str(gameid[i]))
    plt.xticks([])
    plt.yticks([])
    plt.show()

# %%
