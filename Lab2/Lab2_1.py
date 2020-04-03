#import SPI library (for hardware SPI) and MCP3008 library.
import spidev
import os
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
    if "VR_test" in collection_list:
        print("Collection VR_test was found!")
    else:
        mydb.create_collection("VR_test", capped=True, size=500000, max=500)
        print("Create new collection VR_test")
        
        
myclient = pymongo.MongoClient('mongodb://192.168.0.13:27017/')

mydb = myclient["test_database"]

print("Program Start!")

spi = spidev.SpiDev()
spi.open(0,0)

#read SPI data from MCP3008, Channel must be an integer 0-7
def ReadADC(ch):
    if ((ch > 7) or (ch < 0)):
        return -1
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+ch)<<4,0])
    print(adc)
    data = ((adc[1]&3)<<8) + adc[2]
    return data

# Convert data to voltage level
def ReadVolts(data,deci):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,deci)
    return volts

dblist = myclient.list_database_names()

print(dblist)

check_db_exist()
check_collection()
mycol = mydb["VR_test"]

try:
    o_time = time.time()
    while 1:
        if time.time()-o_time >= 1:
            VR_value = ReadADC(0)
            mydict = {"Random_Num": ReadVolts(VR_value, 2), "Time_stamp": time.time()}
            x = mycol.insert_one(mydict)
            print(VR_value)
            print(ReadVolts(VR_value, 2))
            o_time = time.time()
except KeyboardInterrupt:
    print("Bye")


