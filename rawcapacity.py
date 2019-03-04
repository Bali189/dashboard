import re
from pymongo import MongoClient
client = MongoClient()
db = client.Dashboardtest_database
collection = db.Raw_Capacity
collection.remove({})
Total = 0
GrandTotal = 0
ArrayName = ''
record = {}

import os
import time
import datetime
commandlist = []

commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G1000" "serialnum=56660" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G1000" "serialnum=56654" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G1000" "serialnum=56576" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G400" "serialnum=442884" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G600" "serialnum=410367" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G600" "serialnum=410311" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G600" "serialnum=410281" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G600" "serialnum=410246" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G800" "serialnum=442824" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G800" "serialnum=440796" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G800" "serialnum=440757" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G800" "serialnum=440280" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')
commandlist.append('./HiCommandCLI.sh GetStorageArray subtarget=ArrayGroup "model=VSP G800" "serialnum=440237" | grep -e "raidType=RAID" -e diskSize=[1-9] -e name= >> rawcapacity.txt')

def Getrawcapacity():
	# interval = 60 * 5
    isStart = False
    GrandTotal = 0
	for i in commandlist:
		os.system(i)
		time.sleep(interval);
    #/Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/rawcapacity.txt
    for line in open('rawcapacity.txt'):
        line = line.rstrip()
        if('Name' in line):
            if isStart:
                record.pop('_id', None)
                rawcapacity_id = collection.insert_one(record);
                print(rawcapacity_id)
            csv_row = line.split('=')
            record["ArrayName"] = csv_row[1];
            isStart = True;
        elif('raidType' in line):
            csv_row = line.split('=')
            csv_row1 = csv_row[1][6:]
            s = csv_row1.split("+")
            a = int(re.sub('[^0-9]+', '', s[0]))
            b = int(re.sub('[^0-9]+', '', s[1]))
        elif ('diskSize' in line):
            csv_row = line.split('=')
            csv_row1 = str(csv_row[1]).replace(',','')
            csv_row1 = int(csv_row1)
            Total = (a+b)*csv_row1
            GrandTotal = Total + GrandTotal
            record["Capacity"] = GrandTotal
      
	record.pop('_id', None)
    rawcapacity_id = collection.insert_one(record);
    print(rawcapacity_id)

if __name__ == '__main__':
	Getrawcapacity()


