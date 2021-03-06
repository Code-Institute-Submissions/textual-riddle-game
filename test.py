import os
import json
import time
import random

def remove_team_from_file(team_name):
    """Remove a team name from the file"""
    team_name += "\n"
    file = open("data/users.txt","r")
    lines = file.readlines()
    file.close()
    
    file = open("data/users.txt","w")
    for line in lines:
      if line != team_name:
        file.write(line)
        file.close()
  
          


def delete_user_from_board(team,name):
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)
        json1_str[team].pop(name.lower())
    with open("data/scores.json", "w") as file:
          json.dump(json1_str, file, indent=4) 
    #now check if the team is empty. If empty, delete
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)    
        if not len(json1_str[team]):
            json1_str.pop(team)
            with open("data/scores.json", "w") as file:
                  json.dump(json1_str, file, indent=4)
            #now also remove the team name from the text file
            remove_team_from_file(team)

delete_user_from_board("boygroup","gea") 
#remove_team_from_file("bigfoot")

