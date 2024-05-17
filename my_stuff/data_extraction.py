import numpy as np
from utils import *

class ShotDataExtractor():
    def __init__(self):
        self.out_dict = {}
        self.out_dict["agent"] = []
        self.out_dict["teammates"] = []
        self.out_dict["rivals"] = []
        self.out_dict["keeper"] = []
        self.out_dict["goal"] = []
        self.out_dict["predxg"] = []
        self.out_dict["body_part"] = []
        self.out_dict["technique"] = []
        self.out_dict["type"] = []
        self.out_dict["gameid"] = []

    def extractShotData(self, events_file):
        events = open_json(events_file)
        name_file = events_file.split('/')[-1].split('.')[0]
        # find shot events
        shots = []
        for e in events:
            if e["type"]["name"] == "Shot":
                shots.append(e)

        for j in range(len(shots)):
            player_position = shots[j]["location"]
            try:
                frame = shots[j]["shot"]["freeze_frame"]
            except:
                # penalty, we won't use it
                continue
            #print(shots[j]["shot"]["outcome"])
            
            predxg = shots[j]["shot"]["statsbomb_xg"]
            body_part = shots[j]["shot"]["body_part"]["id"]
            techn = shots[j]["shot"]["technique"]["id"]
            type =  shots[j]["shot"]["type"]["id"]

            if shots[j]["shot"]["outcome"]["id"]==97: # goal
                goal = 1
            else:
                goal = 0

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
            self.out_dict["agent"].append([player_position])
            self.out_dict["teammates"].append(teammates.tolist())
            self.out_dict["rivals"].append(rivals.tolist())
            self.out_dict["keeper"].append(keeper.tolist())
            self.out_dict["goal"].append(goal)
            self.out_dict["predxg"].append(predxg)
            self.out_dict["body_part"].append(body_part)
            self.out_dict["technique"].append(techn)
            self.out_dict["type"].append(type)
            self.out_dict["gameid"].append(name_file)
    
    def get_dict(self):
        return self.out_dict
