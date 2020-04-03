import pymongo
import random
import time

def check_db_exist():
    if "test_database" in dblist:
        print("test_database exist!")
    else:
        mycol = mydb["Owner"]
        mydict = {"_id": 0, "name": "Sam", "birthday":"20000327"}
        x = mycol.insert_one(mydict)
        print("Crate database called test_database")
        print("New object crate ID:" + str(x.inserted_id))

def check_collection():
    collection_list = mydb.list_collection_names()
    print(collection_list)
    if "Running_time" in collection_list:
        print("Collection Running_time was found!")
    else:
        mydb.create_collection("Running_time", capped=True, size=1000, max=10)
        print("Create new collection Running_time")
        
        
myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017/')

print("Server Start\n")

mydb = myclient["test_database"]

dblist = myclient.list_database_names()

print(dblist)

check_db_exist()
check_collection()
mycol = mydb["Running_time"]

try:
    o_time = time.time()
    while 1:
        if time.time()-o_time >= 1:
            mydict = {"Random_Num": random.randint(0, 1024), "Time_stamp": time.time()}
            print(mydict)
            x = mycol.insert_one(mydict)
            o_time = time.time()
except KeyboardInterrupt:
    print("Bye")


