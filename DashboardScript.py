# Global Imports
import datetime
import json
import os
import subprocess
from pymongo import MongoClient
if __name__ == "__main__":
    
    try:
        client = MongoClient()
        print("Connected successfully!!!")
    except:  
        print("Could not connect to MongoDB")
    db = client.Dashboardtest_database
    collection = db.Dashboardd
    collection.remove({})
    Dashboard_id = collection.insert_one( { 'Location': "Hillsboro", 'Application': "VPT_Highdensity",'Capacity' : 65.40,'Array': "hb1vsp04" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Noida", 'Application': "Splunk",'Capacity' : 56.45,'Array': "indhds09" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Dublin", 'Application': "HANA_Prod",'Capacity' : 32.40,'Array': "du1hds02" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Sanjose", 'Application': "SAP_Prod",'Capacity' : 10.34,'Array': "sj1hds40" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Hillsboro", 'Application': "Splunk",'Capacity' : 22.35,'Array': "or1hds01" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Hillsboro", 'Application': "Splunk",'Capacity' : 22.35,'Array': "or1hds02" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Dublin", 'Application': "VPT_Lowdensity",'Capacity' : 36.50,'Array': "du1hds02" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Sanjose", 'Application': "HANA_NonProd",'Capacity' : 36.50,'Array': "sj1vsp01" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Hillsboro", 'Application': "DataBase",'Capacity' : 43.35,'Array': "or1hds01" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Sanjose", 'Application': "Engineering",'Capacity' : 86.50,'Array': "sj1hds38" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Noida", 'Application': "SAP_NonProd",'Capacity' : 31.50,'Array': "indhds08" } );
    print(Dashboard_id)
    Dashboard_id = collection.insert_one( { 'Location': "Dublin", 'Application': "SAP_Prod",'Capacity' : 31.50,'Array': "du1hds02" } );
    print(Dashboard_id)
   # NewDashboard = collection.find_one({'_id': Dashboard_id})

    #output = {'Location' :NewDashboard['Location'] ,'Application' :NewDashboard['Application'],'Capacity' :NewDashboard['Capacity'],'Array' :NewDashboard['Array']}
    #print output
    #command = 'df -h'
    #proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
    #stdout_value,stderr_value = proc.communicate()
    #outputlist = stdout_value.splitlines()
    #for i in outputlist:
    #    print i
    #Name = outputlist[0].split(":")[1].strip()

    #Array = outputlist[0].split(":")[0].strip()
    
    #for i,v in enumerate(outputlist):
    #    print v
