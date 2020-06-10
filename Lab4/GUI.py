import tkinter as tk
import seeed_mlx90640


def draw_rectangle(x, y, r, g, b):
    c.create_rectangle(x*10, y*10, (x*10)+9, (y*10)+9, fill=_from_rgb(r, g, b), outline='')
 
def _from_rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

low_t = -150
def temp_color(x, y, temp):
    t = temp - (-150)
    t *= (1020/ 300)
    print("Mapping: "+ str(t))
    r = 0
    g = 0
    b = 0
    if t < 255:
        g = t
        b = 255
    if t >= 255 and t < 510:
        r = (t-255)
        g = 255
    if t >= 510 and t < 765:
        r = 255
        g = (255 - (t-510))
    if t >= 765:
        r = 255
        b = (t-765)
    draw_rectangle(x ,y , int(r), int(g), int(b))

mlx = seeed_mlx90640.grove_mxl90640()
mlx.refresh_rate = seeed_mlx90640.RefreshRate.REFRESH_0_5_HZ


windows = tk.Tk()
windows.title('test')
windows.geometry('500x500')

c = tk.Canvas(windows, width=800 , height=800)
c.grid(row = 0, column = 0)

frame = [0]*768
try:
        mlx.getFrame(frame)

except ValueError:
        print("Error")

x = 0
y = 0
for t in range(0, len(frame)):
    print(frame[t])
    if frame[t] == 'nan':
        frame[t] = low_t
    temp_color(x, y, frame[t])
    x += 1
    if x > 31:
        y += 1
        x = 0
'''
for b in range(0, 255):
    draw_rectangle(x ,y , 0, b, 255)
    x += 1
    if x > 31:
        x = 0
        y += 1

for b in range(0, 255):
    draw_rectangle(x ,y , b, 255, 0)
    x += 1
    if x > 31:
        x = 0
        y += 1

for b in range(255, 0 , -1):
    draw_rectangle(x ,y , 255, b, 0)
    x += 1
    if x > 31:
        x = 0
        y += 1

for b in range(0, 255):
    draw_rectangle(x ,y , 255, 0, b)
    x += 1
    if x > 31:
        x = 0
        y += 1
'''
windows.mainloop()
