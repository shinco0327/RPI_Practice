from smbus2 import SMBus
bus = SMBus(1)
for i in range(0x2440, 0x273F):
    b = bus.read_byte_data(0x33, i)
    print(b)
x = bus.read_word_data(0x33, 0x8000)
print(x)
bus.close()
