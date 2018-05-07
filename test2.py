import os
import json
import time

"""
    for key1, main_value in json1_str.items():
        for key, value in json1_str[key1].items():
            return_val.update({value["Name"].title():value["Scores"]})
"""

def get_names_score_position(return_type,team):
    return_val = {}
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)

    for key1, main_value in json1_str.items():
        for key, value in json1_str[key1].items():
            if key1 == team:
                return_val.update({value["Name"].title():value["Scores"]})

    if return_type == "sorted":#sort result for positions
        return sorted(return_val, key=return_val.get, reverse=True)

    return return_val


    

print(get_names_score_position("sorted","mymine"))