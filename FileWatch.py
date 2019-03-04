import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv
from pymongo import MongoClient
import os

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print "File Modified!"
        if event.is_directory:
            return
        insertdata(event.src_path)

    def on_created(self, event):
        print "File Created ! "
        if event.is_directory:
            return
        insertdata(event.src_path)


if __name__ == "__main__":
    print 'starting'
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/Users/balasubramaniramamurthy/Documents/mypgm/Dashboard/exports/FileToWatch', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    def insertdata(path):
        client = MongoClient()
        db = client.Dashboardtest_database
        collection = db.hitachi_pool
        collection.remove({})
        record={}
        filepath, ext = os.path.splitext(path)
        if (ext == '.csv'):
            line = list()
            with open(path, 'r') as f:
                line = f.readlines()
                line = line.rstrip()
                csv_row = line.split(',')
                for i in csv_row:
                    csv_data = i.split('=')
                    
                    if(len(csv_data)>1):
                        csv_data[0] = csv_data[0].strip()
                        csv_data[1] = csv_data[1].strip()
                        if(csv_data[0] in('Total_Capacity','Free_Capacity')):
                            record [csv_data[0]]= int(csv_data[1])
                        else:
                            record [csv_data[0]]= csv_data[1]

                record.pop('_id', None)
                hitachipool_id = collection.insert_one(record);
                print(hitachipool_id)