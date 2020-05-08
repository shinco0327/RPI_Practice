#import SPI library (for hardware SPI) and MCP3008 library.
import spidev
import os
import pymongo
import random
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
    if "VR_Value" in collection_list:
        print("Collection VR_Value was found!")
    else:
        mydb.create_collection("VR_Value", capped=True, size=500000, max=500)
        print("Create new collection VR_Value")
    if "Temp_Sensor" in collection_list:
        print("Collection Temp_Sensor was found!")
    else:
        mydb.create_collection("Temp_Sensor", capped=True, size=500000, max=500)
        print("Create new collection Temp_Sensor")
        
        
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




check_db_exist()
check_collection()
mycol_vr = mydb["VR_Value"]
mycol_temp = mydb["Temp_Sensor"]


pi = pigpio.pi()
 
x = pi.i2c_open(1, 0x2a)
pi.i2c_write_byte_data(x, 0x54, 0xB6)
pi.i2c_close(x)

try:
    o_time = time.time()
    while 1:
        if time.time()-o_time >= 60:
            VR_value = ReadADC(0)
            mydict = {"sensor_value": ReadVolts(VR_value, 2), "Time_stamp": datetime.datetime.utcnow()}
            x = mycol_vr.insert_one(mydict)
            print("Read of potentiometer is "+VR_value)
            print(ReadVolts(VR_value, 2), "Volts")

            h = pi.i2c_open(1, 0x2a)
            b0 = pi.i2c_read_byte(h)
            time.sleep(0.001)
            b1 = pi.i2c_read_byte(h)
            temp= (256.0*float(b0) + float(b1)) / 100.0
            print("Read of the first byte is "+b0+"\n the second is "+ b1 + "\n The temp is " temp)
            pi.i2c_close(h)
            mydict = {"sensor_value": temp, "Time_stamp": datetime.datetime.utcnow()}
            x = mycol_temp.insert_one(mydict)

            o_time = time.time()
except KeyboardInterrupt:
    print("Bye")
