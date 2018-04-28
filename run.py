import os
import json
import random
from datetime import datetime
import time
import simplejson
from flask import Flask, render_template, request, flash, redirect, url_for
import requests

points = 10
answer_attempts = 0
reg_status = 0
user_reg_state = 0
user_received_question = ""
user_received_answer = ""
status_message = ["Enter a username to start","The Username already exists","Username recorded successfully"]
app = Flask(__name__)
app.secret_key = 'some_secret'
########################################################
########################################################
"""
User information:
When number 0 is returned the user should register.
When number 1 is returned the username chosen already exists
When number 2 is returned the user registration is successful
"""
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
    
def fetch_single_question(id):
    """This is to get a single question."""
    with open("data/questions.json", "r") as questions:
        data = json.load(questions)
        return data[id]
        
def fetch_score_board():
    with open("data/scores.json", "r") as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        return data
    
    
def initiallize_global_variable():
    global points
    global answer_attempts
    global reg_status 
    global user_reg_state 
    global user_received_question
    global user_received_answer   
    
def random_question():
    """This is to generate a random questions and answer combined."""
    with open("data/questions.json", "r") as questions:
        data = json.load(questions)
        return random.choice(data)
            
            
def write_to_file(file_name, data):
    """This function handles all the file writing"""
    with open(file_name, "a") as file:
        file.writelines(data.strip().lower() + "\n") #register the new user and adds a new line

def is_file_empty(file_name):
    if os.path.getsize(file_name) > 0:
        return False
    return True
    
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
def count_users():
    """get number of users available"""
    all_users = 0
    users = []
    with open("data/users.txt", "r") as users_list:
        users = users_list.readlines()
        all_users = len(users)
    return all_users
    
    
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
         
@app.route('/index')
def index_without_post():
   global reg_status
   reg_status = 0 
   info= "None"
   return redirect(url_for('index', user = info)) 
   
@app.route('/index',methods = ['POST', 'GET'])
def index_without_slash():
   """Checks and register new users"""  
   global reg_status
   global user_reg_state
   global user_received_question
   if request.form['user_name']:
       user = request.form['user_name'].strip().title() 
       info = user
       if not does_user_exists(user): #record if the user doese not already exists
          write_to_file("data/users.txt", user)#write username for users file for easy access
          scores_data = {info.lower() :{"Scores": 0, "Name": info , "Time": time.time(), "Questions":[]} }
          write_scores_board("data/scores.json", scores_data)#write username and user data for easy access
          
          reg_status = 2 #status 2 means successful registration
          user_reg_state = 1

       else:
            reg_status = 1
            info = "None"
   else:
       info = "None"
       reg_status = 0

   return redirect(url_for('index',user = info))

def rewrite_json_file(file_name, data):
    with open(file_name, "w") as file:
       json.dump(data, file)
                
def update_scores(name,update,value):
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)
        json1_str[name.lower()]["Time"] = time.time()
        json1_str[name.lower()][update] = json1_str[name.lower()][update] + value
        #json1_str[info.lower()].clear()
    write_scores_board("data/scores.json", json1_str)

    
@app.route('/index/',methods = ['POST', 'GET'])
def index_with_slash():
   """This section will process all answers submitted. And will also test to see if the answer is correct"""
   """Form values
    """  
   info = "None" #Enter a username
   if request.form['userName']:
       global reg_status 
       global user_reg_state 
       info = request.form['userName'].strip().title()
       
       points = int(request.form["pointsReceived"])
       user_reg_state = 1
       reg_status = 2
       update_scores(info,"Scores",points)#scores have updated
   return redirect(url_for('index', user = info)) 
   
@app.route('/')
def index_start():
   """ When a user visits the site directly, the none is used as entry"""
   info = "None" #Prompt to enter a username
   global reg_status 
   return redirect(url_for('index', user = info)) 

@app.route('/<user>')
def index(user):
    global testItCamee
    global reg_status 
    global user_reg_state 
    if user == "":
        user = "None"

    random_questions = random_question()#get the question field
    question_id = random_questions["id"]
    questions_list = [question_id]
    update_scores(user,"Questions",questions_list)#scores have updated  
       
    game_info = {}
    game_info["User"] = user
    game_info["Status"] = reg_status
    game_info["TotalUsers"] = count_users()
    game_info["QuestionsAnswers"] = random_questions
    game_info["Notice"] = status_message
    game_info["UserRegState"] = user_reg_state
    game_info["ScoresBoard"] = get_names_score_position("None")
    game_info["Winners"] = get_names_score_position("sorted")

    #use this to test if it's working as planned

    return render_template("index.html", details = game_info)   

    
########################################################
########################################################
########################################################
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)