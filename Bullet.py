from Actor import Actor
import pygame
import math

class Bullet(Actor):
    SPEED = 0.7

    def __init__(self, coords):
        Actor.__init__(self, pygame.image.load(r'images/bullet-32.png') ,coords)

    def fire(self):
        self.coords[1] -= self.SPEED
    
    def hasCollide(self, impostors):
        for i in range(len(impostors)):
            if math.dist(self.coords, impostors[i].coords) < 20:
                impostors.pop(i)
                return True