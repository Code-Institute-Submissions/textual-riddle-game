import os
import json
import time


def get_names_score_position(return_type):
    return_val = {}
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)
    for key, value in json1_str.items():
        return_val.update({key.title():value["Scores"]})
    #now sort by value rank before returning.

    if return_type == "sorted":
        return sorted(return_val, key=return_val.get, reverse=True)
    return return_val

    
    
print(get_names_score_position("none"))#rename = get_names_score_position()
