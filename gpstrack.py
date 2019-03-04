import csv
from pymongo import MongoClient
client = MongoClient()
db = client.Dashboardtest_database
collection = db.hitachi_pool
collection.remove({})
record={}
hitachitable = []
#for line in open('/Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/hitachi_pool.csv'):
for line in open('/mnt/hitachi_pool.csv'):
    line = line.rstrip()
    csv_row = line.split(',')
    for i in csv_row:
        csv_data = i.split('=')
        
        if(len(csv_data)>1):
            csv_data[0] = csv_data[0].strip()
            csv_data[1] = csv_data[1].strip()
            if(csv_data[0] in('Total_Capacity','Free_Capacity')):
                record [csv_data[0]]= int(csv_data[1])
            elif ('Storage_Name' in csv_data[0]):
                record [csv_data[0]]= csv_data[1]
                if('or1' in csv_data[1]):
                    record["Location"] = 'Hillsboro';
                elif('sj1' in csv_data[1]):
                    record["Location"] = 'Sanjose'
                elif('du' in csv_data[1]):
                    record["Location"] = 'Dublin'
                elif('in' in csv_data[1]):
                    record["Location"]= 'Noida'
            elif(csv_data[0] in 'Pool_Name'):
                record [csv_data[0]]= csv_data[1]
                if(csv_data[1].find('HDT'))!= -1 :
                    isHDT = True
                    record["PoolType"]='HDT'
                elif(csv_data[1].find('HDP') != -1):
                    isHDT = False
                    record["PoolType"]='HDP'
                else:
                    isHDT = False
                    record["PoolType"]=''
            elif (csv_data[0] in 'Storage_Model'):
                record [csv_data[0]]= csv_data[1]
                if(csv_data[1].find('G1000'))!= -1 :
                    record["Tier"] = 'Tier1';
                    record["GSeries"] = 'G1000'
                elif((csv_data[1].find('G800') != -1) or (csv_data[1].find('G600') != -1)):
                    record["GSeries"] = 'GX00'
                    if(isHDT):
                        record["Tier"] = 'Tier1';
                    else:
                        record["Tier"] = 'Tier2';
                else:
                    record["Tier"] = '';
                    record["GSeries"] = ''
                
            else:
                record [csv_data[0]]= csv_data[1]

            #db = client.Dashboardtest_database
    
    record.pop('_id', None)
    print(record)
    hitachipool_id = collection.insert_one(record);
    print(hitachipool_id)     
    #break

hitachipool = list(collection.find())
for i,v in enumerate(hitachipool):
    #print(str(i) +" : "+ str(v))
    TotalCapa = float(hitachipool[i]['Total_Capacity'])/1024/1024/1024
    TotalCapa = round(float(TotalCapa),2)
    FreeCapa = float(hitachipool[i]['Free_Capacity'])/1024/1024/1024
    FreeCapa = round(float(FreeCapa),2)
    
    UsedCapa = round((float(TotalCapa - FreeCapa)),2)
    record1 =   {
                    "StorageModel": hitachipool[i]['Storage_Model'],
                    "PoolName" : hitachipool[i]['Pool_Name'],
                    "StorageName" : hitachipool[i]['Storage_Name'],
                    "TotalCapacity" : TotalCapa,
                    "FreeCapacity" : FreeCapa,
                    "UsedCapacity" : UsedCapa,
                    "Location": hitachipool[i]['Location']
                }
        
    hitachitable.append(record1);
for i in hitachitable:
    print(i)


   