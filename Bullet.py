from Actor import Actor
import pygame
import math

class Bullet(Actor):
    SPEED = 0.7
    direction = -1

    def __init__(self, coords, TYPE):
        if TYPE == "PLAYER":
            Actor.__init__(self, pygame.image.load(r'images/bullet-32.png') ,coords)
        elif TYPE == "ENEMY":
            Actor.__init__(self, pygame.image.load(r'images/enemy-bullet-32.png') ,coords)
            self.direction = 1
            self.SPEED = 0.5

    def fire(self):
        self.coords[1] += self.SPEED * self.direction
    
    def hasCollide(self, impostors):
        for i in range(len(impostors)):
            if math.dist(self.coords, impostors[i].coords) < 25:
                impostors.pop(i)
                return True