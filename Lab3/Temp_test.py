import smbus
import time
import pigpio

print("Program Start!")

address = 0x2a

bus = smbus.SMBus(1)
bus.write_byte(0x2a, 0x54)
bus.wrtie_byte(0x2a, 0xB5)
bus.close()

x = bus.read_i2c_block_data(0x2a, 0x55, 2)

print(x)
