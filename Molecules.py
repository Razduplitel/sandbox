from tkinter import *
from random import randint, uniform
from time import time
from math import *
import matplotlib.pyplot as plt


class Molecule:
    def __init__(self, x, y):
        self.old_x, self.old_y = self.x, self.y = x, y
        self.speed_x, self.speed_y, self.iden = 0, 0, 0

    def draw_particle(self, color):
        # if int(self.old_x) != int(self.x) or int(self.old_y) != int(self.y):
        # field.move(self.iden, int(self.x) - int(self.old_x), int(self.y) - int(self.old_y))
        self.iden = field.create_oval((self.x - radius), (self.y - radius),
                                      (self.x + radius), (self.y + radius),
                                      fill=color, width=0)

    def move(self):
        self.old_x, self.old_y = self.x, self.y
        self.x += self.speed_x
        self.y += self.speed_y

    def border_check(self):
        if self.x > width - radius:
            self.x -= 2 * (self.x - width + radius)
            self.speed_x *= -1
        elif self.x < radius:
            self.x += 2 * (radius - self.x)
            self.speed_x *= -1
        if self.y > height - radius:
            self.y -= 2 * (self.y - height + radius)
            self.speed_y *= -1
        elif self.y < radius:
            self.y += 2 * (radius - self.y)
            self.speed_y *= -1


def force(a, b):
    rx = b.x - a.x
    ry = b.y - a.y
    r2 = rx ** 2 + ry ** 2
    f = eps * 1536 * (128 * radius ** 12 / r2 ** 7 -
                      radius ** 6 / r2 ** 4)
    b.speed_x += rx * f
    b.speed_y += ry * f
    a.speed_x -= rx * f
    a.speed_y -= ry * f


def check():
    for i in range(len(gas) - 1):
        for j in range(i + 1, len(gas)):
            if abs(gas[i].x - gas[j].x) < 5 * radius and \
                    abs(gas[i].y - gas[j].y) < 5 * radius and \
                    (gas[i].x - gas[j].x) ** 2 + (gas[i].y - gas[j].y) ** 2 < 25 * radius ** 2:
                force(gas[j], gas[i])


def pause(event):
    global flag
    flag = False if flag else True
    root.after(50, render)


def render():
    global flag
    if flag:
        global t, fps, energy
        for i in gas:
            i.move()
            i.border_check()
        check()
        en = 0
        for i in gas:
            en += (i.speed_x ** 2 + i.speed_y ** 2)
        energy.append(en)
        field.delete('all')
        for i in gas:
            i.draw_particle('brown')
        t1 = time()
        fps = int(1 / (t1 - t))
        fpss.append(fps)
        root.title('FPS = ' + str(fps))
        t = t1
        root.after(1, render)


def initialization():
    while len(gas) < n:
        mol = Molecule(randint(radius, width - radius), randint(radius, height - radius))
        flag_0 = True
        for i in gas:
            if abs(mol.x - i.x) < 2 * radius:
                if abs(mol.y - i.y) < 2 * radius:
                    if (mol.x - i.x) ** 2 + (mol.y - i.y) < 4 * radius ** 2:
                        flag_0 = False
                        break
        if flag_0:
            gas.append(mol)
    for i in gas:
        fi = uniform(0, 2 * pi)
        v = uniform(speed / 2, speed)
        i.speed_x, i.speed_y = v * cos(fi), v * sin(fi)
    for i in gas:
        i.iden = field.create_oval((i.x - radius), (i.y - radius),
                                   (i.x + radius), (i.y + radius),
                                   fill='brown', width=0)


def window_deleted():
    root.destroy()
    print(sum(fpss) / len(fpss))
    plt.plot([i for i in range(len(energy))], energy, "bo", markersize=1)
    plt.show()


flag = True
energy = []
fpss = []
eps = 1 / 100
width, height, radius = 1300, 800, 16
n, t, fps, speed = 100, time(), 0, radius / 30
root = Tk()
root.geometry('+300+100')
root.protocol('WM_DELETE_WINDOW', window_deleted)
field = Canvas(root, width=width, height=height, bg='silver')
field.pack()
gas = []
initialization()
render()
root.bind('<space>', pause)
root.mainloop()