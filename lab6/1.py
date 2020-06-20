from tkinter import *
from random import randrange as rnd, choice,randint
import time

class Ball:
    global canv, root
    colors = ['red','orange','yellow','green','blue']
    def __init__(self):
        self.x = rnd(100,700)
        self.y = rnd(100,500)
        self.r = rnd(30,50)
        self.color = choice(Ball.colors)
        self.dx = rnd(-3,3)
        self.dy = rnd(-3,3)
        self.ball_id = canv.create_oval(self.x-self.r,
                                   self.y-self.r,
                                   self.x+self.r,
                                   self.y+self.r,fill = self.color, width=0)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x-self.r<0:
            self.dx = -(self.dx)
        if self.x+self.r>800:
            self.dx = -(self.dx)
        if self.y-self.r<0:
            self.dy = -(self.dy)
        if self.y+self.r>600:
            self.dy = -(self.dy)
    
    def show(self):
        canv.move(self.ball_id, self.dx, self.dy)
        root.update()

def tick():
    for ball in balls:
        ball.move()
        ball.show()
    root.after(50, tick)


    
def click(event):
    global points, text, balls
    for ball in balls:
        if (event.y - ball.y)**2 + (event.x - ball.x)**2 <= ball.r**2:
            points += 2
            canv.delete(text)
            canv.delete(ball.ball_id)
            text = canv.create_text(30,20,text=str(points), font = 'Arial 20')    
        else:
            points-=0.2
            canv.delete(text)
            text = canv.create_text(30,20,text=str(points//1), font = 'Arial 20')

def main()   : 
    global root, canv,balls ,points,text    
    root = Tk()
    root.title('My balls')
    root.geometry('800x600')
    canv = Canvas(root,bg='white')
    canv.pack(fill=BOTH,expand=1)
    canv.bind('<Button-1>', click)
    points = 0
    
    text = canv.create_text(30,20,text=0, font = 'Arial 20')
    balls = [Ball() for i in range(5)]
    tick()


    mainloop()

if __name__=='__main__':
    main()

