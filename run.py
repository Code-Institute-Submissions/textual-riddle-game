import os
import json
import random
from datetime import datetime
import time
import simplejson
from flask import Flask, render_template, request, flash, redirect, url_for
import requests

team = ""
user_questions_list = []
points = 10
players = 0
reg_status = 0
user_reg_state = 0
reg_players = 0
status_message = ["Enter a username to start","The Username already exists","Username recorded successfully"]
app = Flask(__name__)
app.secret_key = 'some_secret'
ranks = ["","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th","13th","14th","15th"]

def get_statistics(user):
    global players
    global team  
    global reg_players
    global user_questions_list
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)    
    for key1, main_value in json1_str.items():
           for key, value in json1_str[key1].items():
               if key == user:
                   players = value["Players"]
                   reg_players = value["regPlayers"]
                   team = key1
                   user_questions_list = value["Questions"]
                   
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

def update_scores(team,name,update,value):
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)
        json1_str[team][name.lower()]["Time"] = time.time()
        json1_str[team][name.lower()][update] = json1_str[team][name.lower()][update] + value
        
        #json1_str[info.lower()].clear()
    write_scores_board("data/scores.json", json1_str)

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

def clean_files():
    """When this function is called, it checks for all users that have been inactive for the past 20 minutes and remove their details"""
    minutes_to_evaluate = float(60*20) #20 minutes 
    with open("data/scores.json","r") as json1_file:
        json1_str =  json.load(json1_file)   
        for key1, main_value in json1_str.items():
            for key, value in json1_str[key1].items():
                if (time.time() - main_value[key]["Time"]) > minutes_to_evaluate:
                    delete_user_from_board(key1,key)#a user that has been inactive is deleted.
                    
@app.route('/end_session',methods = ['POST', 'GET'])
def end_session():
   """End the user session"""
   info = "None" #Enter a username
   if request.form.get("userName", False):
       info = request.form['userName'].strip().title()
       team = request.form['team_name'].strip().lower()
       delete_user_from_board(team,info)
       info = "None"     
   return redirect(url_for('index', user = info)) 
   
   
@app.route('/')
def index_start():
   """ When a user visits the site directly, the none is used as entry"""
   clean_files() #clean the files so that users that have been inactive for sometimes are removed.
   info = "None" #Prompt to enter a username
   global team
   global players
   global reg_players
   players = 0
   reg_players = 0
   team = ""
   global reg_status 
   return redirect(url_for('index', user = info)) 
   
   
@app.route('/index')
def index_without_post():
   global reg_status
   global players
   global reg_players
   reg_status = 0 
   info= "None"
   players = 0
   reg_players = 0
   return redirect(url_for('index', user = info)) 
   
@app.route('/index',methods = ['POST', 'GET'])
def index_without_slash():
   """Checks and register new users"""
   global players 
   global reg_players
   if request.form.get("user_name", False):
       user = request.form['user_name'].strip().title() 
       info = user
       players = int(request.form['players'])
       team = request.form['team_name']

       if not does_user_exists(team.lower()): #record if the team does not already exists
          write_to_file("data/users.txt", team.lower())#write team name for users file for easy access
          scores_data = {team.lower():{info.lower() :{"Scores": 0, "Name": info , "Time": time.time(), "Questions":[], "Players":players, "regPlayers":1} }}
          write_scores_board("data/scores.json", scores_data)#write username and user data for easy access
          
          reg_status = 2 #status 2 means successful registration
          user_reg_state = 1
          reg_players  = 0
          
       else:
          #now append the new user to his team
            num = int(request.form['reg_players'])
            reg_players = 1 + num 
            scores_data = {info.lower() :{"Scores": 0, "Name": info , "Time": time.time(), "Questions":[], "Players":players, "regPlayers":reg_players} }
            with open("data/scores.json", "r") as file:
                new = json.load(file)
                new[team.lower()].update(scores_data)
                with open("data/scores.json", "w") as file:
                    json.dump(new, file, indent=4)           
            #write_scores_board("data/scores.json", scores_data)#write username and user data for easy access
            reg_status = 2 #status 2 means successful registration
            user_reg_state = 1   
   else:
       info = "None"
       reg_status = 0
       players = 0
       reg_players = 0

   return redirect(url_for('index',user = info))

@app.route('/index/',methods = ['POST', 'GET'])
def index_with_slash():
   """This section will process all answers submitted."""
   """Form values
    """  
   info = "None" #Enter a username
   if request.form.get("userName", False):
       global reg_status 
       global user_reg_state 
       global team
       global players
       global reg_players
       info = request.form['userName'].strip().title()
       team = request.form['team_name'].strip().lower()
       points = int(request.form["pointsReceived"])
       players = int(request.form["players"])
       reg_players = int(request.form['reg_players'])
       user_reg_state = 1
       reg_status = 2
       
       update_scores(team,info,"Scores",points)#scores have updated

   return redirect(url_for('index', user = info)) 

   
@app.route('/<user>')
def index(user):
    global testItCamee
    global reg_status 
    global user_reg_state
    global players 
    global reg_players
    global user_questions_list

    game_info = {}  
    if user == "None":
        user = "None"
        game_info = {"User":"None","Status":0,"TotalUsers":0,"QuestionsAnswers":{"id": "0","question": "0","answer": "0"}, "Notice":status_message,
          "UserRegState":0,  "ScoresBoard":0,"Winners":"","ranks":0,"Players":0, "regPlayers":0, "HowManyQuestions":0
        }
        reg_players = 0
        return render_template("index.html", details = game_info)  
    else:    
        random_questions = random_question()#get the question field
        question_id = random_questions["id"]
        questions_list = [question_id]

        game_info["User"] = user
        game_info["TotalUsers"] = count_users()
        game_info["QuestionsAnswers"] = random_questions
        game_info["Notice"] = status_message
        game_info["ranks"] = ranks
        game_info["Status"] = reg_status  
        game_info["UserRegState"] = user_reg_state          
        get_statistics(user.lower())#call a function to set the following values into global variables to be available for below
        game_info["Players"] = players
        game_info["Team"] = team
        game_info["regPlayers"] = reg_players  
        game_info["ScoresBoard"] = get_names_score_position("None",team)
        game_info["Winners"] = get_names_score_position("sorted",team)
        all_user_questions = user_questions_list + questions_list
        game_info["HowManyQuestions"] = len(all_user_questions)
        update_scores(team,user,"Questions",questions_list)#scores have updated  
    
        return render_template("index.html", details = game_info)  

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)