# from flask import render_template, Flask, url_for

# app = Flask(__name__)

# @app.route('/hello')
# def hello(name=None):
#   url_for('static', filename='testTags.js')
#   return render_template('search.html')


import csv
from json import dump
# from shutil import copy2
from subprocess import call
import re
import fileinput
import os
from flask import Flask, jsonify, render_template, request, session, redirect, current_app
# from pdfkit import from_url, from_file
app = Flask(__name__)
# from math import ceil
import logging


logging.basicConfig(level=logging.DEBUG)

rootPath = "/var/www/html/semapp/"
# rootPath = "/Users/bchartof/Projects/state-economic-monitor/"
pyPath = "/usr/bin/python"
# pyPath = "/usr/local/bin/python"

@app.route("/update-tasks", methods=["POST", "GET"])
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
def update_SEM():
  # print request.json

  #write a pretty printed json for human readability
  with open(rootPath + 'static/data/cards/prettyCards.json', 'wt') as out:
      res = dump(request.json, out, sort_keys=True, indent=4, separators=(',', ': '))

  #write a one line json for consumption in JS
  with open(rootPath + 'static/data/cards/cards.json', 'wt') as out:
      res = dump(request.json, out, sort_keys=True, separators=(',', ':'))

  os.system(pyPath + " " + rootPath + "reshape.py")
  os.system(pyPath + " " + rootPath + "zipper.py")
  


  return jsonify({})

@app.route('/')
def index():
  return render_template('index.html', name="both")

@app.route('/<name>')
def tasks(name):
  # print(name)
  if(name != "nat" and name != "ben" and name != "both"):
    name = "both"
  return render_template('index.html', name=name)
@app.route('/preferences/<name>')
def preferences(name):
  print(name)
  return render_template('preferences.html', name=name)

if __name__ == '__main__':
  app.debug = True
  app.run(threaded=True)
