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
@app.route('/index')
def index_without_post():
   user = "None"
   return redirect(url_for('index', user = user)) 
   
@app.route('/index',methods = ['POST', 'GET'])
def index_without_slash():
   user = "None"
   if request.form['user_name']:
       user = request.form['user_name']
   """This is to ensure that the index page can be accessed even if it's typed. 
And this section will handle the user registration as well before passing on control 
to the index function """  
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