from random import randrange as rnd, choice
import tkinter as tk
import math
import time


def main():
    global root, canvas, target1, gun, bullet, balls, fr, end_game_screen, c, target2, point, text
    point = 0
    c = 0
    root = tk.Tk()
    fr = tk.Frame(root)
    root.geometry('800x600')
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)
    text = canvas.create_text(30, 30, text=point, font='28')
    target1 = Target()
    target2 = Target()
    end_game_screen = canvas.create_text(400, 300, text='', font='28')
    gun = Gun()
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', gun.prepare_to_shot)
    canvas.bind('<ButtonRelease-1>', gun.take_a_shot)
    canvas.bind('<Motion>', gun.targeting)
    canvas.create_line(0, 600, 800, 600, width=7)


def time_handler():
    global gun, end_game_screen, balls, bullet, target1, target2, point, text
    bullet = 0
    f = 0
    balls = []
    while target1.live or target2.live or balls:
        if target1.live:
            target1.moves()
        if target2.live:
            target2.moves()
        for ball in balls:
            ball.move()
            if ball.hit_test(target1) and target1.live:
                target1.live = 0
                target1.hit()
                f += 1
                point += 1
                canvas.delete(text)
                text = canvas.create_text(30, 30, text=point, font='28')
            if ball.hit_test(target2) and target2.live:
                target2.live = 0
                target2.hit()
                f += 1
                point += 1
                canvas.delete(text)
                text = canvas.create_text(30, 30, text=point, font='28')
            canvas.update()
            time.sleep(0.03)
            gun.targeting()
    canvas.delete(gun)


class Ball:
    def __init__(self, x, y, vx, vy):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 1
        self.var_x = 0

    def set_coords(self):
        """ Меняет координаты мяча (вспомогательная ф-ция для move()
        """
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def gravity(self):
        global c
        """if self.y + self.r <= 597:
            self.vy -= 3
        else:
            self.vy = -self.vy

        self.vx *= 0.999
        """
        self.vy += 2
        if self.y >= 590:
            c += 1
        if c == 20:
            self.vy = 0

    def reflection(self):
        """ Функция реализует отражение мяча от стен
        """
        if self.x + self.r >= 800 or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r >= 600:
            self.vy = -self.vy/1.2

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        self.gravity()
        self.reflection()
        self.set_coords()

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (abs(obj.x - self.x) <= (obj.r + self.r) and
                abs(obj.y - self.y) <= (obj.r + self.r)):
            return True
        return False


class Gun:
    def __init__(self):
        """ Устанавливает начальные параметры пушки
        """
        self.f2_power = 10
        self.f2_on = 0
        self.angel = 1
        self.x = 20
        self.y = 450
        self.id = canvas.create_line(self.x, self.y, 50, 420, width=7)

    def prepare_to_shot(self, event):
        """ Подготовка выстрела
        """
        self.f2_on = 1

    def take_a_shot(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        x = 20 + max(self.f2_power, self.x) * math.cos(self.angel)
        y = 450 + max(self.f2_power, self.x) * math.sin(self.angel)
        self.angel = math.atan((event.y - self.y) / (event.x - self.x))
        vx = self.f2_power * math.cos(self.angel)
        vy = self.f2_power * math.sin(self.angel)
        new_ball = Ball(x, y, vx, vy)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angel = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.angel),
                      450 + max(self.f2_power, 20) * math.sin(self.angel)
                      )

    def power_up(self):
        """ Удлинение пушки

        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.live = 1

        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r)
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)
        self.vy = rnd(-5, 5)

    def hit(self):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)

    def set_place(self):
        """ Меняет координаты мяча (вспомогательная ф-ция для move()
        """
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def reflect(self):
        if self.y + self.r >= 600 or self.y - self.r <= 0:
            self.vy = -self.vy

    def moves(self):
        self.y += self.vy
        self.reflect()
        self.set_place()


main()

time_handler()

tk.mainloop()
