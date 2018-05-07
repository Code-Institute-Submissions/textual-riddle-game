import os
import json
import random
from datetime import datetime
import time
from flask import Flask, render_template, request, flash, redirect, url_for
import requests

            
def write_to_file(file_name, data):
    """This function handles all the file writing"""
    with open(file_name, "a") as file:
        file.writelines(data.strip().lower() + "\n") #register the new user and adds a new line


def is_file_empty(file_name):
    if os.path.getsize(file_name) > 0:
        return False
    return True
    
    
def does_user_exists(username):
    """This is to check if user exists. To ensure multiple registration is not permitted"""
    if username == "" or username == " ":#empty or space should return true. Registration not allowed
       return True
    users = []
    with open("data/users.txt", "r") as user_file: #This open the file for reading
       users = user_file.readlines()
       username += "\n"
       if username.lower() in users:
          return True
       else:
          return False

def write_scores_board(file_name, data): #this may be removed.
    """ This function writes json files"""
    if is_file_empty(file_name):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)            

    else:
        with open(file_name, "r") as file:
            new = json.load(file)
            new.update(data)
            with open(file_name, "w") as file:
                json.dump(new, file, indent=4)
#Get total users   


user = "Bello3" 
info = user
players = 3
team = "jerks3"



scores_data = {info.lower() :{"Scores": 0, "Name": info , "Time": time.time(), "Questions":[], "Players":players} }
with open("data/scores.json", "r") as file:
    new = json.load(file)
    new[team].update(scores_data)
    with open("data/scores.json", "w") as file:
        json.dump(new, file, indent=4)          
                    
                    
reg_status = 2 #status 2 means successful registration
user_reg_state = 1  
if not does_user_exists(team): #record if the team does not already exists
     write_to_file("data/users.txt", team)#write team name for users file for easy access

          
def delete_user_from_board(team,name):
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)
        json1_str[team][name.lower()].pop()

    with open("data/scores.json", "w") as file:
          json.dump(json1_str, file, indent=4)    
        #json1_str[info.lower()].clear()
    #write_scores_board("data/scores.json", json1_str)

delete_user_from_board("braingroup","richie")          