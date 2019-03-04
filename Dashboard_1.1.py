# Global Imports
import collections
import csv
import datetime
import json
import os
import pdb
import dateutil.parser
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


	# Home Page
@app.route("/", methods=['GET', 'POST'])
def main():
	"""Main Function, home page"""
	client = MongoClient()
	print("Connected successfully!!!")
	db = client.Dashboardtest_database
	collection = db.Dashboardd
	Location_Selected = ''
	Application_Selected = ''
	Array_Selected = ''		
	if request.method == 'POST':
		try:
			outputtable = []
			outputchart =[]
			outputchartloc =[]
			outputhitachitier = []
			outputhitachi = []
			outputhitachitype = []
			outputhitachitypepool=[]
			outputrawcapacity = []
			Location_Selected = request.form['ddlLocation']
			Application_Selected = request.form['ddlApplication']
			Array_Selected = request.form['ddlArray']
			MatchQuery = {}
			# { "$match": {"Application":Application_Selected,"Location":Location_Selected ,"Array" : Array_Selected} },
			SelectedLoc = {}
			if 'Global' not in Location_Selected:
				SelectedLoc["Location"] = Location_Selected
			if 'Global' not in Application_Selected:
				SelectedLoc["Application"] = Application_Selected
			if 'Global' not in Array_Selected:
				SelectedLoc["Array"] = Array_Selected
			MatchQuery["$match"] = SelectedLoc
			ReportDashboard = list(collection.aggregate([MatchQuery,
									{ "$sort": { 'Application': 1 }}
									]))
			for i, value in enumerate(ReportDashboard):
				record =   {
							"Location": ReportDashboard[i]['Location'],
							"Capacity" : ReportDashboard[i]['Capacity'],
							"Application" : ReportDashboard[i]['Application'],
							"Array" : ReportDashboard[i]['Array']
					}
			
				outputtable.append(record);
			Reportgroup = list(collection.aggregate([MatchQuery,
									{ "$group" : { "_id" : "$Application" , 
									"totalcapacity": { "$sum" : "$Capacity" }}},
									{ "$sort": { '_id': 1 }}
									]))
			for i, value in enumerate(Reportgroup):
				record1 =   {
							"Application": Reportgroup[i]['_id'],
							"Capacity" : Reportgroup[i]['totalcapacity']
					}
				outputchart.append(record1)

			collectionpool = db.hitachi_pool
			hitachipool = list(collectionpool.aggregate([
										{ "$group" : { "_id" : "$Location" , 
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipool):
				TotalCapa = float(hitachipool[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipool[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record2 =   {
								"Location" : hitachipool[i]['_id'],
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc
							}
					
				outputhitachi.append(record2)


			hitachipooltier = list(collectionpool.aggregate([
				 						{"$match" : { 'Tier' : 'Tier1'}},
										{ "$group" : { "_id" : "$Storage_Name" ,
   										"Tier" : { "$first": '$Tier'} ,
										"GSeries" : { "$first": '$GSeries'} ,
										"Location" : { "$first": '$Location'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltier):
				TotalCapa = float(hitachipooltier[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltier[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record3 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Location" : hitachipooltier[i]['Location'],
								"Tier" : hitachipooltier[i]['Tier'],
								"GSeries" : hitachipooltier[i]['GSeries'],
								"Array":hitachipooltier[i]['_id']
							}
				outputhitachitier.append(record3)
			
			hitachipooltierGseries = list(collectionpool.aggregate([
				 						{"$match" : { 'Tier' : 'Tier2'}},
										{ "$group" : { "_id" : "$Storage_Name" ,
   										"Tier" : { "$first": '$Tier'} ,
										"Location" : { "$first": '$Location'} ,
										"GSeries" : { "$first": '$GSeries'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltierGseries):
				TotalCapa = float(hitachipooltierGseries[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltierGseries[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record4 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Location" : hitachipooltierGseries[i]['Location'],
								"Tier" : hitachipooltierGseries[i]['Tier'],
								"GSeries" : hitachipooltierGseries[i]['GSeries'],
								"Array":hitachipooltierGseries[i]['_id']
							}
				outputhitachitier.append(record4)
				

			hitachipooltype = list(collectionpool.aggregate([
										{ "$group" : { "_id" : "$Storage_Name" , 
										"PoolType" : { "$first": '$PoolType'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltype):
				TotalCapa = float(hitachipooltype[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltype[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record4 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Array" : hitachipooltype[i]['_id'],
								"PoolType" : hitachipooltype[i]['PoolType']
							}
					
				outputhitachitype.append(record4)


			#HDT HDP

			hitachipooltypePool = list(collectionpool.aggregate(
                    [
                        {
                            "$group" : { 
                                "_id" : "$Storage_Name",
                                "HDT-TotalCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDT" ] },
                                        "$Total_Capacity",0] }},
                                "HDT-FreeCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDT" ] },
                                        "$Free_Capacity",0] }},
                                "HDP-TotalCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDP" ] },
                                        "$Total_Capacity",0] }},
                                "HDP-FreeCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDP" ] },
                                        "$Free_Capacity",0] }}
                        }
                },{ "$sort": { '_id': 1 }}
				]))

			for i,v in enumerate(hitachipooltypePool):
				TotalCapaHDT = float(hitachipooltypePool[i]['HDT-TotalCapacity'])/1024/1024/1024
				TotalCapaHDT = round(TotalCapaHDT,2)
				FreeCapaHDT = float(hitachipooltypePool[i]['HDT-FreeCapacity'])/1024/1024/1024
				FreeCapaHDT = round(FreeCapaHDT,2)
				UsedCapaHDT = round((TotalCapaHDT - FreeCapaHDT),2)
				

				TotalCapaHDP = float(hitachipooltypePool[i]['HDP-TotalCapacity'])/1024/1024/1024
				TotalCapaHDP = round(TotalCapaHDP,2)
				FreeCapaHDP = float(hitachipooltypePool[i]['HDP-FreeCapacity'])/1024/1024/1024
				FreeCapaHDP = round(FreeCapaHDP,2)
				
				UsedCapaHDP = round((TotalCapaHDP - FreeCapaHDP),2)
				
				record5 =   {
								"TotalCapacity - HDT" : TotalCapaHDT,
								"FreeCapacity - HDT": FreeCapaHDT,
								"UsedCapacity - HDT" : UsedCapaHDT,
								"TotalCapacity - HDP" : TotalCapaHDP,
								"FreeCapacity - HDP": FreeCapaHDP,
								"UsedCapacity - HDP" : UsedCapaHDP,
								"Location" : hitachipooltypePool[i]['_id']
							}
					
				outputhitachitypepool.append(record5)

			collectionrawcapacity = db.Raw_Capacity
			rawcapacity = list(collectionrawcapacity.aggregate([
							{ "$group" : { "_id" : "$ArrayName" , 
							"Capacity": { "$sum" : "$Capacity" }}},
							{ "$sort": { '_id': 1 }}
							]))
			for i,v in enumerate(rawcapacity):
				record6 =   {
								"Capacity" : rawcapacity[i]['Capacity'],
								"Array" : rawcapacity[i]['_id']
							}
					
				outputrawcapacity.append(record6)


		except Exception as ex:  
			print("Could not connect to MongoDB + Error :   " ,ex)
	elif request.method == 'GET':
		try:
			outputtable = []
			outputchart =[]
			outputchartloc =[]
			outputhitachi =[]
			outputhitachitier = []
			outputhitachitype = []
			outputhitachitypepool=[]
			outputrawcapacity = []

			ReportDashboard = list(collection.aggregate([
									{ "$sort": { 'Application': 1 }}
									]))
			

			Reportgroup = list(collection.aggregate([
										{ "$group" : { "_id" : "$Application" , 
										"totalcapacity": { "$sum" : "$Capacity" }}},
										{ "$sort": { '_id': 1 }}
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


			collectionpool = db.hitachi_pool
			

			hitachipool = list(collectionpool.aggregate([
										{ "$group" : { "_id" : "$Location" , 
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipool):
				TotalCapa = float(hitachipool[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipool[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record2 =   {
								"Location" : hitachipool[i]['_id'],
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc
							}
					
				outputhitachi.append(record2)


			hitachipooltier = list(collectionpool.aggregate([
				 						{"$match" : { 'Tier' : 'Tier1'}},
										{ "$group" : { "_id" : "$Storage_Name" ,
   										"Tier" : { "$first": '$Tier'} ,
										"GSeries" : { "$first": '$GSeries'} ,
										"Location" : { "$first": '$Location'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltier):
				TotalCapa = float(hitachipooltier[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltier[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record3 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Location" : hitachipooltier[i]['Location'],
								"Tier" : hitachipooltier[i]['Tier'],
								"GSeries" : hitachipooltier[i]['GSeries'],
								"Array":hitachipooltier[i]['_id']
							}
				outputhitachitier.append(record3)
			
			hitachipooltierGseries = list(collectionpool.aggregate([
				 						{"$match" : { 'Tier' : 'Tier2'}},
										{ "$group" : { "_id" : "$Storage_Name" ,
   										"Tier" : { "$first": '$Tier'} ,
										"Location" : { "$first": '$Location'} ,
										"GSeries" : { "$first": '$GSeries'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltierGseries):
				TotalCapa = float(hitachipooltierGseries[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltierGseries[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record4 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Location" : hitachipooltierGseries[i]['Location'],
								"Tier" : hitachipooltierGseries[i]['Tier'],
								"GSeries" : hitachipooltierGseries[i]['GSeries'],
								"Array":hitachipooltierGseries[i]['_id']
							}
				outputhitachitier.append(record4)
				

			hitachipooltype = list(collectionpool.aggregate([
										{ "$group" : { "_id" : "$Storage_Name" , 
										"PoolType" : { "$first": '$PoolType'} ,
										"TotalCapacity": { "$sum" : "$Total_Capacity" },
										"FreeCapacity": { "$sum" : "$Free_Capacity" }}},
										{ "$sort": { '_id': 1 }}
										]))
			for i,v in enumerate(hitachipooltype):
				TotalCapa = float(hitachipooltype[i]['TotalCapacity'])/1024/1024/1024
				TotalCapa = round(TotalCapa,2)
				FreeCapa = float(hitachipooltype[i]['FreeCapacity'])/1024/1024/1024
				FreeCapa = round(FreeCapa,2)
				
				UsedCapa = round((TotalCapa - FreeCapa),2)
				usedperc = round(float(UsedCapa/TotalCapa)*100,2)
				record4 =   {
								"TotalCapacity" : TotalCapa,
								"FreeCapacity": FreeCapa,
								"UsedCapacity" : UsedCapa,
								"Used %" : usedperc,
								"Array" : hitachipooltype[i]['_id'],
								"PoolType" : hitachipooltype[i]['PoolType']
							}
					
				outputhitachitype.append(record4)


			#HDT HDP

			hitachipooltypePool = list(collectionpool.aggregate(
                    [
                        {
                            "$group" : { 
                                "_id" : "$Storage_Name",
                                "HDT-TotalCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDT" ] },
                                        "$Total_Capacity",0] }},
                                "HDT-FreeCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDT" ] },
                                        "$Free_Capacity",0] }},
                                "HDP-TotalCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDP" ] },
                                        "$Total_Capacity",0] }},
                                "HDP-FreeCapacity": {"$sum": {
                                "$cond": [{ "$eq": [ "$PoolType",   "HDP" ] },
                                        "$Free_Capacity",0] }}
                        }
                },{ "$sort": { '_id': 1 }}
				]))

			for i,v in enumerate(hitachipooltypePool):
				TotalCapaHDT = float(hitachipooltypePool[i]['HDT-TotalCapacity'])/1024/1024/1024
				TotalCapaHDT = round(TotalCapaHDT,2)
				FreeCapaHDT = float(hitachipooltypePool[i]['HDT-FreeCapacity'])/1024/1024/1024
				FreeCapaHDT = round(FreeCapaHDT,2)
				UsedCapaHDT = round((TotalCapaHDT - FreeCapaHDT),2)
				

				TotalCapaHDP = float(hitachipooltypePool[i]['HDP-TotalCapacity'])/1024/1024/1024
				TotalCapaHDP = round(TotalCapaHDP,2)
				FreeCapaHDP = float(hitachipooltypePool[i]['HDP-FreeCapacity'])/1024/1024/1024
				FreeCapaHDP = round(FreeCapaHDP,2)
				
				UsedCapaHDP = round((TotalCapaHDP - FreeCapaHDP),2)
				
				record5 =   {
								"TotalCapacity - HDT" : TotalCapaHDT,
								"FreeCapacity - HDT": FreeCapaHDT,
								"UsedCapacity - HDT" : UsedCapaHDT,
								"TotalCapacity - HDP" : TotalCapaHDP,
								"FreeCapacity - HDP": FreeCapaHDP,
								"UsedCapacity - HDP" : UsedCapaHDP,
								"Location" : hitachipooltypePool[i]['_id']
							}
					
				outputhitachitypepool.append(record5)


			collectionrawcapacity = db.Raw_Capacity
			rawcapacity = list(collectionrawcapacity.aggregate([
							{ "$group" : { "_id" : "$ArrayName" , 
							"Capacity": { "$sum" : "$Capacity" }}},
							{ "$sort": { '_id': 1 }}
							]))
			for i,v in enumerate(rawcapacity):
				record6 =   {
								"Capacity" : rawcapacity[i]['Capacity'],
								"Array" : rawcapacity[i]['_id']
							}
					
				outputrawcapacity.append(record6)

		except Exception as ex:  
			print("Error :   " ,ex)  
			

	return render_template('reportsnew.html',outputrawcapacity=outputrawcapacity,outputhitachitypepool = outputhitachitypepool,outputhitachitype = outputhitachitype,outputhitachitier = outputhitachitier,output = outputtable,outputchart = outputchart,outputhitachi = outputhitachi,Location_Selected=Location_Selected,Application_Selected = Application_Selected,Array_Selected=Array_Selected)

# Inventory Page
@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
	client = MongoClient()
	print("Connected successfully!!!")
	db = client.Dashboardtest_database
	ReportDashboard_Inventory=[]
	Report_Inventory=[]
	collection = db.Dashboard_Report
	ReportDashboard_Inventory = list(collection.find())
	for i, value in enumerate(ReportDashboard_Inventory):
		if(ReportDashboard_Inventory[i]['Support Expiry'] =='SN?'):
			d = ''
		else:
			d = str(ReportDashboard_Inventory[i]['Support Expiry'])
			d = dateutil.parser.parse(d).date()
		record =   {
						"Location": ReportDashboard_Inventory[i]['Location'],
						"Device Name" : ReportDashboard_Inventory[i]['Device Name'],
						"Device Type" : ReportDashboard_Inventory[i]['Device Type'],
						"Site ID" : ReportDashboard_Inventory[i]['Site ID'],
						"Device Model" : ReportDashboard_Inventory[i]['Device Model'],
						"Pri IP Address" : ReportDashboard_Inventory[i]['IP Address'],
						"Pri Serial Number" : ReportDashboard_Inventory[i]['Serial Number'],
						"Install/Purchase" : ReportDashboard_Inventory[i]['Install/Purchase'],
						"Support Expiry" : d
				  }
		Report_Inventory.append(record)

	
	return render_template('inventory.html',ReportDashboard_Inventory = Report_Inventory)
	
# Historic Data Page
@app.route("/histdata", methods=['GET', 'POST'])
def histdata():
	if request.method == 'POST':
		return render_template('histdata.html')
	elif request.method == 'GET':
		return render_template('histdata.html')

if __name__ == '__main__':
		app.run(debug=False, host='127.0.0.1')
