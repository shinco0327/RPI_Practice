import seeed_mlx90640
import time

mlx = seeed_mlx90640.grove_mxl90640()
mlx.refresh_rate = seeed_mlx90640.RefreshRate.REFRESH_8_HZ

frame = [0] * 768
while True:
    start = time.time()
    try:
        mlx.getFrame(frame)
    except ValueError:
        continue
    print(frame)
    end = time.time()
    
