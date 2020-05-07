import pigpio 
import time
#Baudrate in /boot/config.txt is set to 25000

pi = pigpio.pi()
 
x = pi.i2c_open(1, 0x2a)
pi.i2c_write_byte_data(x, 0x54, 0xB6)
pi.i2c_close(x)

while 1:
    h = pi.i2c_open(1, 0x2a)
    b0 = pi.i2c_read_byte(h)
    time.sleep(0.001)
    b1 = pi.i2c_read_byte(h)
    print(b0)
    print(b1)
    print( (256.0*float(b0) + float(b1)) / 100.0)
    pi.i2c_close(h)
    time.sleep(1)
