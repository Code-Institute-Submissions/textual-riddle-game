import os
import json
import time
def is_file_empty(file_name):
    if os.path.getsize(file_name) > 0:
        return False
    return True
def write_scores_board(file_name, data): #this may be removed.
    """ This function writes json files"""
    if is_file_empty(file_name):

        with open(file_name, "w") as file:
            json.dump(data, file)            
    else:
        with open(file_name, "r") as file:
            new = json.load(file)
            new.update(data)
            with open(file_name, "w") as file:
                json.dump(new, file)

info = "Genome"
scores_data = {info:{"Scores": 0, "Name": info, "Time": time.time(), "Questions":[]} }
write_scores_board("data/scores.json", scores_data)#write username and user data for easy access
with open("data/scores.json","r") as json1_file:
       #json1_file = open("data/scores.json","r")
       #print("Json File: ",  json1_file)
       #json1_str = json1_file.read()
       json1_str =  json.load(json1_file)
       json1_str[info]["Name"] = "Fate"
       print("Json String File: ", len(json1_str))
       print(json1_str[info]["Name"])
       
with open("data/scores.json","w") as file:
       json.dump(json1_str,file)
       
       
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