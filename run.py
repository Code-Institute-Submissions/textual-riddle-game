import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'
########################################################
########################################################
########################################################
def write_to_file(file_name, data):
    """This function handles all the file writing"""
    with open(file_name, "a") as file:
        file.writelines(data + "\n") #register the new user and adds a new line
        
def does_user_exists(username):
    """This is to check if user exists. To ensure multiple registration is not permitted"""
    with open("data/users.txt", "r") as user_file: #This open the file for reading
       users = []
       with open("data/users.txt", "r") as users_list:
           users = users_list.readlines()
           if username in users:
               return True
           else:
              return False


        
        
@app.route('/index')
def index_without_post():
   user = "None"
   return redirect(url_for('index', user = user)) 
   
@app.route('/index',methods = ['POST', 'GET'])
def index_without_slash():
   """Checks and register new users"""  
   user = "None" #This is the default user.
   if request.form['user_name']:
       user = request.form['user_name']
       if not does_user_exists(user): #record if the user doese not already exists
          write_to_file("data/users.txt", user)
   
   return redirect(url_for('index',user = user))
   
@app.route('/index/')
def index_with_slash():
   user = "None"
   return redirect(url_for('index', user = user)) 
   
@app.route('/')
def index_start():
   """ When a user visits the site directly, the none is used as entry"""
   user = "None"
   return redirect(url_for('index', user = user)) 

@app.route('/<user>')
def index(user):
    if user == "":
        user = "None"
    return render_template("index.html", name = user)   
      
########################################################
########################################################
########################################################
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)