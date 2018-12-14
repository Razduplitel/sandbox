from tkinter import *
#from random import randint

def fill_cell(i, j, size, color):
    field.create_rectangle(i * size, j * size, (i + 1) * size, (j + 1) * size, outline='black', fill=color, width=1)

def fill_all(f, size):
    for i in range(len(f)):
        for j in range(len(f[0])):
            fill_cell(i, j, size, 'white' if f[i][j] == 0 else 'black')

def around(f, i, j):
    sum = 0
    for p in range(-1, 2):
        for q in range(-1, 2):
            sum += f[(i+p)%len(f)][(j+q)%len(f[0])]
    return sum - f[i][j]

def refresh():
    global f
    f1 = []
    for i in range(len(f)):
        f1 = f1 + [[]]
        for j in range(len(f[0])):
            f1[i] = f1[i] + [[]]
            if around(f, i, j) == 3 or f[i][j] == 1 and around(f, i, j) == 2:
                f1[i][j] = 1
            else:
                f1[i][j] = 0
            if f1[i][j] != f[i][j]:
                yield (i, j, f1[i][j])
    f = f1

flag = False

def rebuild():
    FPS = fps.get()
    global flag
    if flag == True:
        for cell in refresh():
            fill_cell(cell[0], cell[1], size, 'white' if cell[2] == 0 else 'black')
        root.update()
        root.after(1000 // FPS, rebuild)

def pause(event):
    global flag
    flag = False if flag == True else True
    root.after(1000 // FPS, rebuild)

def draw(event):
    a, b  = event.x // size, event.y // size
    f[a][b] = 0 if f[a][b] == 1 else 1
    fill_cell(a, b, size, 'white' if f[a][b] == 0 else 'black')

#def rand_fill(event):
#    global f
#    for i in range(len(f)):
#        for j in range(len(f[0])):
#            f[i][j] = randint(0, 1)
#            fill_cell(i, j, size, '#fff' if f[i][j] == 0 else '#000')

root = Tk()
width, height, size, FPS = 50, 30, 10, 20
field = Canvas(root, width=width * size, height=height * size, bg ='white')
field.pack(side='left')
fps = Scale(root, orient=VERTICAL, length=height*size, from_=1, to=25, tickinterval=24, resolution=1)
fps.set(15)
fps.pack(side='right')
f = [[0 for j in range(height)] for i in range(width)]      # f[i][j]: i - row, j -column
f[1][1] = f[2][2] = f[2][3] = f[3][1] = f[3][2] = 1

fill_all(f, size)
root.bind('<space>', pause)
field.bind('<Button-1>', draw)
#root.bind('<Button1-Motion>', draw)
#root.bind('<Control-r>', rand_fill)
root.after(1000 // FPS, rebuild)
root.mainloop()
