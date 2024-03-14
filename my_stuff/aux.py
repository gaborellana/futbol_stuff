import json
import numpy as np


def open_json(json_file):
    with open(json_file) as json_f:
        data = json.load(json_f)
    return data

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
        try:
            frame = shots[j]["shot"]["freeze_frame"]
        except:
            # penalty, we won't use it
            continue
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

