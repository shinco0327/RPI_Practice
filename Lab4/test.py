import MLX90640 as x
import math

x.setup(16)
f = x.get_frame()
x.cleanup()

print(f)

for x in f:
    if math.isnan(x) == True:
        print("Failed Pixel")    
