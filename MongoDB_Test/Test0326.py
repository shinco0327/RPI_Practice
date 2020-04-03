import pymongo

myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017/')

print("Server Start\n")

mydb = myclient["test_database"]

dblist = myclient.list_database_names()

print(dblist)

if "test_database" in dblist:
    print("test_database exist!")
else:
    mycol = mydb["Owner"]
    mydict = {"_id": 0, "name": "Sam", "birthday":"20000327"}
    x = mycol.insert_one(mydict)
    print("Crate database called test_database")
    print("New object crate ID:" + str(x.inserted_id))
    

