# Global Imports
import collections
import csv
import datetime
import json
import os
import pdb
#import urllib.parse


# Flask Imports
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import flash
from flask_pymongo import PyMongo
from flasgger import Swagger
from flasgger.utils import swag_from

# HTML Specific Imports
from wtforms import Form
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import MacAddress
from pymongo import MongoClient

# Setup Flask API APP
app = Flask(__name__)
Swagger(app)
# Web Form Class for HTML
class ReusableForm(Form):
  mac_addr = (
    TextField('MAC Address:', validators=[validators.MacAddress(message=None)])
  )


  # Home Page
@app.route("/", methods=['GET', 'POST'])
def main():
  """Main Function, home page"""
  
      
  if request.method == 'POST':
    try:
      outputtable = []
      outputchart =[]
      Location_Selected = request.form['ddlLocation']
      if(Location_Selected =='Global'):
        ReportDashboard = list(collection.find())
        for i, value in enumerate(ReportDashboard):
          record =   {
                "Location": ReportDashboard[i]['Location'],
                "Capacity" : ReportDashboard[i]['Capacity'],
                "Application" : ReportDashboard[i]['Application'],
                "Array" : ReportDashboard[i]['Array']
            }
        
          outputtable.append(record);

        Reportgroup = list(collection.aggregate([
                    { "$group" : { "_id" : "$Application" , 
                    "totalcapacity": { "$sum" : "$Capacity" }}}
                    ]))
        for i, value in enumerate(Reportgroup):
          record1 =   {
                "Application": Reportgroup[i]['_id'],
                "Capacity" : Reportgroup[i]['totalcapacity']
            }
          outputchart.append(record1)
      elif( 'Global' not in Location_Selected):
        cursor = list(collection.find({"Location":Location_Selected}))
        for i, value in enumerate(cursor):
	        record =   {
                "Location": cursor[i]['Location'],
                "Capacity" : cursor[i]['Capacity'],
                "Application" : cursor[i]['Application'],
                "Array" : cursor[i]['Array']}
          outputtable.append(record)
          return render_template('reports.html',output = outputtable,outputchart = outputchart)
    except:  
      print("Error in application")
  elif request.method == 'GET':
    try:
      client = MongoClient()
      print("Connected successfully!!!")
      db = client.Dashboardtest_database
      collection = db.Dashboardd
      
      outputtable = []
      outputchart =[]

      ReportDashboard = list(collection.find())
      Reportgroup = list(collection.aggregate([
                    { "$group" : { "_id" : "$Application" , 
                    "totalcapacity": { "$sum" : "$Capacity" }}}
                    ]));

      for i, value in enumerate(Reportgroup):
        record1 =   {
                "Application": Reportgroup[i]['_id'],
                "Capacity" : Reportgroup[i]['totalcapacity']
            }
        outputchart.append(record1);
      for i, value in enumerate(ReportDashboard):
        
        record =   {
                "Location": ReportDashboard[i]['Location'],
                "Capacity" : ReportDashboard[i]['Capacity'],
                "Application" : ReportDashboard[i]['Application'],
                "Array" : ReportDashboard[i]['Array']
            }
        
        outputtable.append(record);
      
  except:  
      print("Could not connect to MongoDB")

    return render_template('reports.html',output = outputtable,outputchart = outputchart)


# Inventory Page
@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
  if request.method == 'POST':
    return render_template('inventory.html')
  elif request.method == 'GET':
    return render_template('inventory.html')

# Historic Data Page
@app.route("/histdata", methods=['GET', 'POST'])
def histdata():
  if request.method == 'POST':
    return render_template('histdata.html')
  elif request.method == 'GET':
    return render_template('histdata.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
