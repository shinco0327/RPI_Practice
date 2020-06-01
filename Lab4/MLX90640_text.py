import seeed_mlx90640
mlx = seeed_mlx90640.grove_mxl90640()
mlx.refresh_rate = seeed_mlx90640.RefreshRate.REFRESH_0_5_HZ
#/boot/config.txt i2c baudrate=50K

frame = [0]*768
try:
    mlx.getFrame(frame)
    print(frame)
    count = 0
    for i in frame:
        if i == 'nan' or i <= 20 or i>= 35:
            print(i)
            count+=1
    print("Broken Pixels = "+ str(count))
except ValueError:
    print("Error")
    


