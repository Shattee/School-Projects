# 1. Draw one particle shooting to the middle of canvas and then explode
# 2. add multiple particles with random location around the original shooting particle into a list
# 3. Draw these particles to simulate firework explosion

import math
import random
from tkinter import *

root = Tk()       # create tkinter window
window = Canvas(root, width=800, height=600)
window.pack()
window['background'] = 'black'
random.seed(1)    # make the random results fixed

# functions to generate random color as rgb format
def rgb2hex(r, g ,b):
    return '#%02x%02x%02x' % (r, g, b)
def randomColor():
    r = math.floor(random.random() * 255)
    g = math.floor(random.random() * 255)
    b = math.floor(random.random() * 255)
    return rgb2hex(r, g, b)


gravity = 0.3


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.random() * 4 - 2
        self.vy = random.random() * 4 - 1
        self.color = color
        self.explode = False
        self.lifespan = 100  # particle will disappear when lifespan = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += gravity

        if self.y > 600 or self.lifespan <= 0:  # if the particle is outside window or lifespan reaches 0
            self.explode = True

    def sparking(self):
        size = 1  # the size of spark
        window.create_oval(self.x - size, self.y - size,
                           self.x + size, self.y + size, fill=self.color, outline=self.color)



# the single particle before explode
class firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = random.randint(-18, -10)    # make it explode at different location
        self.explode = False
        self.color = randomColor()
        self.lifespan = 100
    def shooting(self):   # draw particle
        window.create_oval(self.x-2, self.y-2, self.x+2, self.y+2, fill=self.color)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += gravity

        if self.vy >= 0:
            self.explode = True

particles = []
fireworks = []

def fireup():
    while len(fireworks) < 5:       # refill the fireworks list if number of fireworks are below 5
        fireworks.append(firework(random.randint(0, 800), 600))  # rise from random location at the bottom of the window
    window.delete("all")           # refresh the window
    for ii in range(0, len(fireworks)):
        if ii >= len(fireworks) - 1:   # make sure ii is not out of index
            break
        f = fireworks[ii]
        if f.explode:     # generate random numbers of sparks
            for jj in range(0, random.randint(50, 70)):
                particles.append((Particle(f.x, f.y, f.color)))
            fireworks.pop(ii)      # delete the original shooting spark
        f.update()    # keep the shooting particle moving
        f.shooting()

    # display sparks after explode
    for ii in range(0, len(particles)):
        if ii >= len(particles) - 1:
            break
        p = particles[ii]
        if p.explode:
            particles.pop(ii)
        p = particles[ii]
        p.update()
        p.lifespan -= random.randrange(1, 7)        # lifespan=0 particles will disappear
        p.sparking()

    root.after(40, fireup)  # 40ms delay for calling fireup function another time

# initialize the fireworks
fireup()
root.mainloop()
