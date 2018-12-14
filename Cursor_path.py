from math import sqrt
from tkinter import *
from time import time

root = Tk()
x0, y0, L = 0, 0, 0
t = time()


def window_deleted():
    t1 = time()
    with open("output.txt", "a") as f:
        f.write(str(round(L * 0.0001796875, 2)) + " meters in " + str(round(t1 - t)) + " seconds\n")
        f.write(str(round(L)) + " pixels in " + str(round(t1 - t)) + " seconds\n")
        f.write(str(round(L / (t1 - t), 1)) + " pix per sec\n\n")
    root.destroy()


def motion(event):
    global x0, y0, L
    L += sqrt((event.x_root-x0)**2+(event.y_root-y0)**2)
    x0, y0, = event.x_root, event.y_root
    print(int(L))


root.protocol('WM_DELETE_WINDOW', window_deleted)
root.bind('<Motion>', motion)
root.attributes('-fullscreen', True)
root.grab_set_global()
root.update()
root.iconify()
root.attributes('-fullscreen', False)
root.geometry('0x0+0+0')
root.mainloop()