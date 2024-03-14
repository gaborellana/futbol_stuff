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
def open_json(json_file):
    with open(json_file) as json_f:
        data = json.load(json_f)
    return data


# %%
events360aux = open_json(files[0])

# open event file
matchid = files[0].split("/")[-1]
events_path = "/home/gablinux/futbol_db/events/"
events_file = events_path + matchid

eventsaux = open_json(events_file)

# %%

events = []
events360 = []

indx = 0
for i in range(len(events360aux)):
    ev360 = events360aux[i]
    for j in range(indx,len(events360aux)):
        ev = eventsaux[j]
        if ev["id"] == ev360["event_uuid"]:
            flg = 1
            events.append(ev)
            events360.append(ev360)
            break
    if flg:
        indx = j

print(len(events), len(events360))
print(len(eventsaux), len(events360aux))
del eventsaux, events360aux

# %%
#example first coincidence
ev = events[0]
ev3 = events360[0]

print(ev)
print(ev3)
print(ev["type"]["name"])

# %%

frames = []
for j in range(200):
    eventj = events360[j]
    players=eventj["freeze_frame"]
    actor = []
    teammates = []
    rivals = []
    keeper = []
    typeev = []
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
    typeev = events[j]["type"]["name"] + " - " + events[j]["id"]
    actor = np.array(actor)
    teammates = np.array(teammates)
    rivals = np.array(rivals)
    keeper = np.array(keeper)
    frames.append([actor, teammates, rivals, keeper, typeev])

# %%
frames_path = "/home/gablinux/futbol_db/frames/"

# %%

for j in range(len(frames)):
    frame = frames[j]
    actor = frame[0]
    teammates = frame[1]
    rivals = frame[2]
    keeper = frame[3]
    typeev = frame[4]

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
    plt.title(typeev)
    plt.close(fig)

    fig.savefig(frames_path + "frame_{}.png".format(str(j)))




# %%
# find shot events
shots = []
for e in events:
    if e["type"]["name"] == "Shot":
        shots.append(e)
    
# %%
j = 0
player_position = shots[j]["location"]
frame = shots[j]["shot"]["freeze_frame"]
print(shots[j]["shot"]["outcome"])

teammates = []
rivals = []
keeper = []
typeev = []
for i in range(len(frame)):
    if frame[i]["position"]["id"]==1:
        keeper.append(frame[i]["location"])
    else:
        if frame[i]["teammate"]:
            teammates.append(frame[i]["location"])
        else:
            rivals.append(frame[i]["location"])
teammates = np.array(teammates)
rivals = np.array(rivals)
keeper = np.array(keeper)


# %%
for j in range(len(shots)):
    player_position = shots[j]["location"]
    frame = shots[j]["shot"]["freeze_frame"]
    #print(shots[j]["shot"]["outcome"])
# %%
# extracting shot data from events

def extractShotData(events_file):
    events = open_json(events_file)
    # find shot events
    shots = []
    for e in events:
        if e["type"]["name"] == "Shot":
            shots.append(e)

    output = []
    for j in range(len(shots)):
        player_position = shots[j]["location"]
        frame = shots[j]["shot"]["freeze_frame"]
        #print(shots[j]["shot"]["outcome"])
        
        if shots[j]["shot"]["outcome"]["id"]==97: # goal
            target = 1
        else:
            target = 0

        teammates = []
        rivals = []
        keeper = []
        for i in range(len(frame)):
            if frame[i]["position"]["id"]==1:
                keeper.append(frame[i]["location"])
            else:
                if frame[i]["teammate"]:
                    teammates.append(frame[i]["location"])
                else:
                    rivals.append(frame[i]["location"])
        teammates = np.array(teammates)
        rivals = np.array(rivals)
        keeper = np.array(keeper)
        out_array = [player_position, teammates.tolist(), rivals.tolist(), 
                     keeper.tolist(), target]
        output.append(out_array)
    return output

out = extractShotData(events_file)

# %%

print(len(out))
x = 1
print(out[-1][x])
print(type(out[-1][x]))

# %%
for i in out:
    print(i)
# %%
