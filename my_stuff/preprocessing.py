
import json
import numpy as np
from utils import *

# calculate X, L, F, target from processed data
# X: positions of players
# L: role labels of players (0 for attacker, 1 for defender, 2 for goalkeeper)
# F: additional features for the entire shot (type, techn, body_part)
# target: binary label indicating if the shot resulted in a goal (0 or 1)

def calculate_prefeatures(proc_json_file, ndecimals = 4):
    data = open_json(proc_json_file)
    
    out_dict= {}
    out_dict["agent"] = []
    out_dict["teammates"] = []
    out_dict["rivals"] = []
    out_dict["keeper"] = []
    out_dict["goal"] = []
    out_dict["predxg"] = []
    out_dict["body_part"] = []
    out_dict["technique"] = []
    out_dict["type"] = []
    out_dict["positions"] = []
    out_dict["roles"] = []
    out_dict["distances"] = []
    out_dict["angles"] = []
    out_dict["gameid"] = []
    
    for i in range(len(data)):
        dati = data[i]

        out_dict["agent"].append(dati["agent"])
        out_dict["teammates"].append(dati["teammates"])
        out_dict["rivals"].append(dati["rivals"])
        out_dict["keeper"].append(dati["keeper"])
        out_dict["goal"].append(dati["goal"])
        out_dict["predxg"].append(dati["predxg"])
        out_dict["body_part"].append(dati["body_part"])
        out_dict["technique"].append(dati["technique"])
        out_dict["type"].append(dati["type"])
        out_dict["gameid"].append(dati["gameid"])
        
        labels =["agent", "teammates", "rivals", "keeper"]
        L = [list( j*np.ones(len(dati[labels[j]])).astype(int) ) for j in range(4)]
        L = np.concatenate(L, axis=0)
        X = []
        for j in range(4):
            if dati[labels[j]]==[]:
                continue
            X.append(dati[labels[j]])
        X = np.concatenate(X, axis=0)
        # L: array length of players, content: ints with codification of roles(positions)
        # X: array length of players, content: arrays len=2 with positions of players X,Y 

        # calculate distances and angles between players
        D = np.zeros([len(X),len(X)])
        A = np.zeros([len(X),len(X)])
        for i in range(len(X)):
            for j in range(len(X)):
                D[i,j] = np.linalg.norm(X[i]-X[j]).astype(np.float16)
                A[i,j] = np.arctan2(X[i,1]-X[j,1], -(X[i,0]-X[j,0])).astype(np.float16)
        
        out_dict["positions"].append(np.around(X, decimals=ndecimals).tolist())
        out_dict["roles"].append(np.around(L, decimals=ndecimals).tolist())
        out_dict["distances"].append(np.around(D, decimals=ndecimals).tolist())
        out_dict["angles"].append(np.around(A, decimals=ndecimals).tolist())

    output_name = proc_json_file.replace('.json', '_features.json')
    with open(output_name, 'w') as f:
        json.dump(out_dict, f)    



proc_json_file = "/home/gablinux/futbol_db/shots_data/shots_db.json"
calculate_prefeatures(proc_json_file)


