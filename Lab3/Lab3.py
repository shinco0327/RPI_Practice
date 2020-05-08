import pymongo
import time
import pigpio
import datetime

def check_db_exist():
    dblist = myclient.list_database_names()
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
    if "Temp_Sensor" in collection_list:
        print("Collection Temp_Sensor was found!")
    else:
        mydb.create_collection("Temp_Sensor", capped=True, size=500000, max=500)
        print("Create new collection Temp_Sensor")
        
        
myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017/')

mydb = myclient["test_database"]

print("Program Start!")

check_db_exist()
check_collection()
mycol = mydb["Temp_Sensor"]

pi = pigpio.pi()
 
x = pi.i2c_open(1, 0x2a)
pi.i2c_write_byte_data(x, 0x54, 0xB6)
pi.i2c_close(x)
try:
    o_time = time.time()
    while 1:
        if time.time()-o_time >= 1:


            h = pi.i2c_open(1, 0x2a)
            b0 = pi.i2c_read_byte(h)
            time.sleep(0.001)
            b1 = pi.i2c_read_byte(h)
            print(b0)
            print(b1)
            temp= (256.0*float(b0) + float(b1)) / 100.0
            print(temp)
            pi.i2c_close(h)
            mydict = {"sensor_value": temp, "Time_stamp": datetime.datetime.utcnow()}
            x = mycol.insert_one(mydict)
            o_time = time.time()
except KeyboardInterrupt:
    print("Bye")


