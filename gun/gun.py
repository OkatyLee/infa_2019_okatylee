from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))


class Ball:
    def __init__(self, obj):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = obj.x1
        self.y = obj.y1
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coordinates(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.reflect()
        self.gravity()
        self.live -= 0.4
        self.x += self.vx
        self.y -= self.vy
        self.set_coordinates()
        self.killer()

    def reflect(self):
        """Отвечает за отражение от стен
        """
        if self.x >= 800 - self.r:
            self.vx = self.vx * -0.5
            self.x -= self.r
        if self.y + self.r >= 600:
            self.vy = - self.vy * 0.7
            self.y -= self.r

    def gravity(self):
        """"Отвечает за гравитацию
        """
        if self.y + self.r < 590 and self.live > 0:
            self.vy -= 1

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(self.x - obj.x) <= self.r + obj.r and abs(self.y - obj.y) <= self.r + obj.r:
            return True
        return False

    def killer(self):
        """"Убирает шарики с экрана
        """
        global balls
        if self.live <= 0:
            balls.pop(0)
            canvas.delete(self.id)
            self.vx = 0
            self.vy = 0


class Gun:
    """Конструктор класса пушка
    """
    def __init__(self):
        self.x1 = 20
        self.y1 = 450
        self.x2 = 50
        self.y2 = 420
        self.gun_length = 10
        self.trigger = 0
        self.an = 1
        self.id = canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=7)
        self.live = 1

    def prepare_to_shot(self, event):
        """"Отвечает за обраюотку нажатия ЛКМ
        """
        if event:
            self.trigger = 1
        else:
            self.trigger = 0

    def shot(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, gun
        bullet += 1
        new_ball = Ball(gun)
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.gun_length * math.cos(self.an)
        new_ball.vy = - self.gun_length * math.sin(self.an)
        balls += [new_ball]
        self.trigger = 0
        self.gun_length = 10

    def targeting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-self.y1) / (event.x-20))
        if self.trigger:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x1, self.y1,
                      self.x1 + max(self.gun_length, self.x1) * math.cos(self.an),
                      self.y1 + max(self.gun_length, self.x1) * math.sin(self.an)
                      )

    def power_up(self):
        """"Отвечает за увеличение размеров пушки и изменение цвета
        """
        if self.trigger:
            if self.gun_length < 100:
                self.gun_length += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            self.gun_length = 10
            canvas.itemconfig(self.id, fill='black')

    def set_coordinates(self):
        canvas.coords(
                self.id,
                self.x1,
                self.y1,
                self.x1 + max(self.gun_length, self.x1) * math.cos(self.an),
                self.y1 + max(self.gun_length, self.x1) * math.sin(self.an)
                )

    def move_upper(self, event):
        if event:
            self.y1 -= 10
            self.y2 -= 10
            self.set_coordinates()

    def move_lower(self, event):
        if event:
            self.y1 += 10
            self.y2 += 10
            self.set_coordinates()

    def move_right(self, event):
        if event:
            self.x1 += 10
            self.x2 += 10
            self.set_coordinates()


class Target:
    """"Конструктор класса Цель
    """
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.new_target()
        self.color = 'red'
        self.x = 0
        self.y = 0
        self.r = 0
        self.direction = rnd(0, 1)
        self.vy = rnd(5, 15)
        if self.direction:
            self.vy = -self.vy

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 50)
        color = self.color = 'red'
        canvas.coords(self.id, x-r, y-r, x+r, y+r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)

    def set_coordinates(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
                )

    def move(self):
        """Двигает цели по вертикали
        """
        if self.live:
            if self.y + self.r > 590 - self.r or self.y - self.r < self.r + 10:
                self.vy = -self.vy
                self.y += self.vy
            self.y += self.vy
            self.set_coordinates()


class Bomb:
    def __init__(self):
        """"Конструктор класса Бомба
        """
        self.r = 20
        self.x = 790
        self.y = rnd(20, 580)
        self.vx = rnd(10, 20)
        self.id = canvas.create_oval(self.x - self.r,
                                     self.y - self.r,
                                     self.x + self.r,
                                     self.y + self.r,
                                     fill='white')

    def set_coordinates(self):
        canvas.coords(self.id,
                      self.x - self.r,
                      self.y - self.r,
                      self.x + self.r,
                      self.y + self.r,
                      )

    def move(self):
        """Отвечает за движение бомбы
        """
        self.x -= self.vx
        self.set_coordinates()
        if self.x + self.r < 0:
            self.kill_create()

    def hit(self, obj):
        """Проверяет столкновение с obj
        """
        if self.x - self.r <= (obj.x2+obj.x1)//2 <= self.x + self.r:
            if(min(obj.y1, obj.y2) <= self.y + self.r <= max(obj.y1, obj.y2) or
               min(obj.y1, obj.y2) <= self.y - self.r <= max(obj.y1, obj.y2) or
               self.y == obj.y1 or self.y == obj.y2 or self.y == (obj.y1 + obj.y2)//2):
                return True
        return False

    def kill_create(self):
        if self.x + self.r < 0:
            canvas.delete(self.id)
        self.x = 790
        self.y = rnd(20, 580)
        self.vx = rnd(10, 20)
        self.id = canvas.create_oval(self.x - self.r,
                                     self.y - self.r,
                                     self.x + self.r,
                                     self.y + self.r,
                                     fill='Black')


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
t1 = Target()
t2 = Target()
screen1 = canvas.create_text(400, 300, text='', font='28')
bullet = 0
gun = Gun()
balls = []
bombs = [Bomb() for i in range(3)]
points = 0
str_point = canvas.create_text(30, 30, text=points, font='28')


def new_game(event=''):
    global gun, t1, screen1, balls, bullet, t2, points, bombs
    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', gun.prepare_to_shot)
    canvas.bind('<ButtonRelease-1>', gun.shot)
    canvas.bind('<Motion>', gun.targeting)
    root.bind('<w>', gun.move_upper)
    root.bind('<s>', gun.move_lower)
    root.bind('<d>', gun.move_right)
    t1.live = 1
    t2.live = 1
    while (t1.live or balls or t2.live) and gun.live:
        t1.move()
        t2.move()
        for bomb in bombs:
            bomb.move()
        for b in balls:
            b.move()
            if b.hit_test(t1) and t1.live:
                t1.live = 0
                t1.hit()
                points += 1
                canvas.itemconfig(str_point, text=points)
            if b.hit_test(t2) and t2.live:
                t2.live = 0
                t2.hit()
                points += 1
                canvas.itemconfig(str_point, text=points)
            if t1.live == 0 and t2.live == 0:
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        time.sleep(0.03)
        if gun.live:
            gun.targeting(event)
            gun.power_up()
    canvas.itemconfig(screen1, text='')
    if gun.live:
        canvas.delete(gun)
    root.after(2, new_game)


new_game()

root.mainloop()
