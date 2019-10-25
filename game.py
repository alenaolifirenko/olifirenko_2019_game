from tkinter import *
from random import randrange as rnd

# Стартовые условия игры:

N = 50
U1 = 23

v = 500
vr = 50
stop = 1
T = 10
gravity = 0.2
r_area = 5

x_min = 50  # расположение по x
x_max = 1500
y_min = 50  # расположение по у
y_max = 650
r_min = 10  # макс и мин радиусы
r_max = 30
x_border_min = 50  # граничные условия для шариков
x_border_max = 1450
y_border_min = 50
y_border_max = 700

score = 0  # начальный счёт игрока
BALLS = [None] * N  # пустой массив шариков
flag = True

# Задаём цвета шариков и их количество (N <= len(colors)):
colors = [
    '#FFCCB6', '#CBAACB', '#FF968A',
    '#55CBCD', '#97C1A9', '#ECD5E3', '#FFFFB5',
    '#FFCCB6', '#CBAACB', '#FF968A', '#55CBCD',
    '#97C1A9', '#ECD5E3', '#FFCCB6']


# Обновление стартовых условий
def Update_Constants():
    global x_b, y_b, r_b, v_x, v_y
    x_b = [rnd(x_min, x_max) for i in range(N)]
    y_b = [rnd(y_min, y_max) for i in range(N)]
    r_b = [rnd(r_min, r_max) for i in range(N)]
    v_x = [rnd(-v, v + 1) / 100 for i in range(N)]
    v_y = [rnd(-v, v + 1) / 100 for i in range(N)]


# Открытие файла на запись:
if flag:
    f = open('Score table.txt', 'w')
    dict_score = {}

# Оформление полотна:
root = Tk()
root.geometry('1500x700')
canv = Canvas(root, bg='#00506B')
canv.pack(fill=BOTH, expand=1)

# Добавление пользователя и счёта:
empty_name = 'ВВЕДИТЕ ИМЯ'
name = empty_name

ent = Entry(width=20)
ent.pack(side=RIGHT)

but_ent = Button(text="Сменить пользователя")
but_ent.pack(side=RIGHT)

but_save = Button(text="Save")
but_save.pack(side=LEFT)

label = Label(text="User: " + name,
              font='Courier 20')
label.pack()


# Смена пользователя
def Add_user(event):
    global name
    if ent.get():
        name = ent.get()
    else:
        name = empty_name
        print(name)


# Сохранение результатов пользователя и обновление игры
def Save(event):
    global score, lvl, flag
    name_new = {str(name): str(score)}
    dict_score.update(name_new)
    names = list(dict_score)
    f = open('Score table.txt', 'w')
    for i in range(len(dict_score)):
        f.write(names[i] + " " + dict_score[names[i]] + "\n")
    Update_Constants()
    Ball.new_ball(N, x_b, y_b, r_b, v_x, v_y)
    flag = False


# Функционал программы:
class Ball:
    def __init__(self, i, _x, _y, _r, _v_x, _v_y, color='black'):
        self.v_x = _v_x
        self.v_y = _v_y
        self.x = _x
        self.y = _y
        self.r = _r
        self.color = color
        self.ball = canv.create_oval(
            _x - _r, _y - _r,
            _x + _r, _y + _r,
            fill=color, width=0,
            activefill='#FC7F0D',
            tag='ball' + str(i))

    def new_ball(N, x_b, y_b, r_b, v_x, v_y):
        for i in range(N):
            canv.delete('ball' + str(i))
            BALLS[i] = Ball(i,
                            x_b[i], y_b[i],
                            r_b[i],
                            v_x[i], v_y[i],
                            colors[i % len(colors)])

    def update():
        global BALLS
        for i in range(U1):
            BALLS[i].v_y += gravity
            BALLS[i].color = '#FFB5E8'
            BALLS[i].r = 10

            if BALLS[i].y > 690:
                BALLS[i].v_y = - rnd(1, 5) * v / 100

            if BALLS[i].v_x ** 2 + BALLS[i].v_y ** 2 > 10 ** 2:
                BALLS[i].v_y = 0
                BALLS[i].v_x = 0
                BALLS[i].r *= 0.9

        for i in range(N):
            BALLS[i].x += BALLS[i].v_x
            BALLS[i].y += BALLS[i].v_y
            # ограничение по х
            if BALLS[i].x > x_border_max:
                BALLS[i].v_x *= - stop
                BALLS[i].x = x_border_max
            if BALLS[i].x < x_border_min:
                BALLS[i].v_x *= -stop
                BALLS[i].x = x_border_min

            # ограничение по y
            if BALLS[i].y > y_border_max:
                BALLS[i].v_y *= -stop
                BALLS[i].y = y_border_max
            if BALLS[i].y < y_border_min:
                BALLS[i].v_y *= -stop
                BALLS[i].y = y_border_min

            canv.delete('ball' + str(i))
            BALLS[i] = Ball(i,
                            BALLS[i].x, BALLS[i].y,
                            BALLS[i].r,
                            BALLS[i].v_x, BALLS[i].v_y,
                            BALLS[i].color)

        root.after(T, Ball.update)


def click(event):
    global score
    x_e = event.x
    y_e = event.y
    for i in range(N):
        rho = (BALLS[i].x - x_e) ** 2 + (BALLS[i].y - y_e) ** 2
        if rho <= (BALLS[i].r + r_area) ** 2:
            if i < U1:
                score += 5
            else:
                score += 1
            BALLS[i].x = rnd(x_min, x_max)
            BALLS[i].y = rnd(y_min, y_max)
            BALLS[i].v_x = rnd(-v, v) / 100
            BALLS[i].v_y = rnd(-v, v) / 100


def tick():
    label.config(
        text="User: " + name + ", score = " + str(score),
        font='Courier 20')
    label.after(200, tick)


Update_Constants()
Ball.new_ball(N, x_b, y_b, r_b, v_x, v_y)
Ball.update()


def OFF(event):
    global score, v_x, v_y, x_min, x_max, y_max, y_min
    score = 0
    x_min = event.x - 25  # расположение по x
    x_max = x_min + 25
    y_min = event.y - 25  # расположение по x
    y_max = y_min + 25
    Update_Constants()
    Ball.new_ball(N, x_b, y_b, r_b, v_x, v_y)
    x_min = 50  # расположение по x
    x_max = 1500
    y_min = 50  # расположение по у
    y_max = 650


# Привязка клавиш:
label.after_idle(tick)
canv.bind('<Button-1>', click)
canv.bind('<Button-2>', OFF)
but_ent.bind('<Button-1>', Add_user)
but_save.bind('<Button-1>', Save)

root.mainloop()
