import tkinter as tk


def draw_rectangle(x, y, r, g, b):
    c.create_rectangle(x*10, y*10, (x*10)+9, (y*10)+9, fill=_from_rgb(r, g, b), outline='')
 
def _from_rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


windows = tk.Tk()
windows.title('test')
windows.geometry('500x500')

c = tk.Canvas(windows, width=800 , height=800)
c.grid(row = 0, column = 0)

x= 0
y = 0
for b in range(0, 255):
    draw_rectangle(x ,y , 0, b, 255)
    x += 1
    if x > 31:
        x = 0
        y += 1
'''
for b in range(0, 255):
    draw_rectangle(x ,y , b, 255, 0)
    x += 1
    if x > 31:
        x = 0
        y += 1
'''
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

windows.mainloop()
