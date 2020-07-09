import tkinter as tk
import MLX90640 as mlx
import math
import threading
import time

def get_Temp():
    while 1:
        try: 
            print("Scaning")
            global frame
            frame = mlx.get_frame()
        except ValueError:
            print("ReadError") 

def draw_rectangle(x, y, r, g, b):
    c.create_rectangle(x*10, y*10, (x*10)+10, (y*10)+10, fill=_from_rgb(r, g, b), outline='')
 
def _from_rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def temp_color(x, y, temp, limt_temp):
    t = temp - limt_temp
    t *= (765/ 12)
    if t >= 765:
        t = 764
    else:
        t = int(t)
   # print("Mapping: "+ str(t))
    r = 0
    g = 0
    b = 0
    if t < 255:
        g = t
        b = 255
    if t >= 255 and t < 510:
        r = 255
        g = 255 - (t-255)
    if t >= 510:
        r = 255
        b = (t-510)
    draw_rectangle(x ,y , int(r), int(g), int(b))

mlx.setup(32)


windows = tk.Tk()
windows.title('test')
windows.geometry('500x500')

c = tk.Canvas(windows, width=800 , height=800)
c.grid(row = 1, column = 0)


label_frame = tk.Frame(windows)
label_frame.grid(row=0, column=0, sticky='w')
low_label = tk.Label(label_frame, text="Lowest Temp: ")
low_label.grid(row= 0, column=0, sticky='w')

high_label = tk.Label(label_frame, text="Highest Temp: ")
high_label.grid(row=1, column=0, sticky='w')

center_label = tk.Label(label_frame)
center_label.grid(row=2, column=0, sticky='w')

thread1 = threading.Thread(target = get_Temp)
thread1.start()

def loop_Process():
    try:
        x = 0
        y = 0
        low_temp = 1000.0
        high_temp = -100
        for i in frame:
            if float(i) < low_temp:
                low_temp = i
            if float(i) > high_temp:
                high_temp = i

        for t in range(0, len(frame)):
            # print(frame[t])
            if math.isnan(frame[t]) == True:
                frame[t] = low_temp
            temp_color(x, y, frame[t], low_temp)
            x += 1
            if x > 31:
                y += 1
                x = 0
        low_label.configure(text=('Lowest Temp=' + str("%2f" % low_temp)))
        high_label.configure(text=('Highest Temp= '+ str("%2f" % high_temp)))
        center_label.configure(text=('Center Temp= '+ str("%2f" % frame[384])))
    except Exception as e:
        pass
    windows.after(5, loop_Process)
    

windows.after(5, loop_Process)

windows.mainloop()
mlx.cleanup()
