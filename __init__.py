# from flask import render_template, Flask, url_for

# app = Flask(__name__)

# @app.route('/hello')
# def hello(name=None):
#   url_for('static', filename='testTags.js')
#   return render_template('search.html')


import csv
from json import dump, load
# from shutil import copy2
from subprocess import call
import re
import fileinput
from flask import Flask, jsonify, render_template, request, session, redirect, current_app, Response, url_for, abort
# from pdfkit import from_url, from_file
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
app = Flask(__name__)
# from math import ceil
import logging
from os import getenv, system
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

rootPath = "/var/www/html/semapp/"
# rootPath = "/Users/bchartof/Projects/state-economic-monitor/"
pyPath = "/usr/bin/python"
# pyPath = "/usr/local/bin/python"



load_dotenv('.env')


# config
app.config.update(
    DEBUG = True,
    # SECRET_KEY = getenv('SECRET_KEY'),
    NAT_LOGIN = getenv('NAT_LOGIN'),
    BEN_LOGIN = getenv('BEN_LOGIN')
)
# print(app.config)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "nat" if id == 0 else "ben"
        self.password = app.config.get(self.name.upper() + "_LOGIN")
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20       
users = [User(id) for id in range(0, 1)]



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']       
        if password == app.config.get(username.upper() + "_LOGIN"):
            name = username
            user = User(name)
            login_user(user, remember=True)
            return redirect(name)
        else:
            return abort(401)
    else:
        return render_template("login.html")



# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('error.html', error="You have been successfully logged out on this computer")


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('error.html', error="Invalid username or password")
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)




@app.route("/update-tasks", methods=["POST", "GET"])
@login_required
def updateTasks():
  if request.method == 'POST':
    # file = request.files['file']
    # sheet = request.args.get('sheet', '', type=str)
    # print sheet
    # file.save(rootPath + "static/data/source/" + sheet + ".xlsx")
    # print(request.data)
    with open("static/data/tasks.json","wt") as out:
      res = dump(request.json, out, sort_keys=True, indent=4, separators=(',', ': '))

  return ""

@app.route('/add', methods=["POST", "GET"])
@login_required
def update_SEM():
  # print request.json

  #write a pretty printed json for human readability
  with open(rootPath + 'static/data/cards/prettyCards.json', 'wt') as out:
      res = dump(request.json, out, sort_keys=True, indent=4, separators=(',', ': '))

  #write a one line json for consumption in JS
  with open(rootPath + 'static/data/cards/cards.json', 'wt') as out:
      res = dump(request.json, out, sort_keys=True, separators=(',', ':'))

  system(pyPath + " " + rootPath + "reshape.py")
  system(pyPath + " " + rootPath + "zipper.py") \
  


  return jsonify({})

@app.route('/')
@login_required
def index():
  return tasks("both")
#   return render_template('index.html', name="both")

@app.route('/<name>')
@login_required
def tasks(name):
  # print(name)
  if(name != "nat" and name != "ben" and name != "both"):
    name = "both"


  return render_template('index.html', name=name)

@app.route('/preferences/<name>')
@login_required
def preferences(name):
  print(name)
  return render_template('preferences.html', name=name)

if __name__ == '__main__':
  app.debug = True
  app.secret_key = getenv('SECRET_KEY')
  app.run(threaded=True)
