#!/usr/bin/python2.7

from Tkinter import *
import random
import time

class wall:
  def __init__(self, x0, y0, x1, y1):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1

def update(root, canvas, wall, hx, hy, px, py):

  canvas.delete(ALL)
  for i in wall:
    if i:
      canvas.create_line(i.x0+50, i.y0+50, i.x1+50, i.y1+50)

  canvas.create_line(50, 50, 550, 50, width = 1)
  canvas.create_line(50, 50, 50, 550, width = 1)
  canvas.create_line(550, 50, 550, 550, width = 1)
  canvas.create_line(50, 550, 550, 550, width = 1)
  hx += 50
  hy += 50
  px += 50
  py += 50

  canvas.create_oval(hx-4, hy-4, hx+4, hy+4, fill='red')
  canvas.create_oval(px-1, py-1, px+1, py+1, fill='blue')    

  canvas.update()
#  time.sleep(.05)


def main(): 
  root = Tk()
  root.title('Evasion')

  canvas = Canvas(root, width = 600, height = 600, bg = 'white')
  canvas.pack()    

  canvas.create_line(50, 50, 550, 50, width = 1)
  canvas.create_line(50, 50, 50, 550, width = 1)
  canvas.create_line(550, 50, 550, 550, width = 1)
  canvas.create_line(50, 550, 550, 550, width = 1)
  hx, hy = 50, 50
  px, py = 320, 200
  hunter = canvas.create_rectangle(hx-4, hy-4, hx+4, hy+4, fill='red')
  prey = canvas.create_oval(px-1, py-1, px+1, py+1, fill='blue')    
  canvas.update()
  return root, canvas
  #---  
  time.sleep(5)
  w = [wall(100, 200, 100, 300)]
  update(root, canvas, w, 300, 300, 500, 500)
  time.sleep(1)

  
#main()
